Déploiement et CI/CD
====================

Vue d'ensemble
--------------

Orange County Lettings utilise une chaîne de déploiement automatisée basée sur
Docker, GitHub Actions, Docker Hub et Render.

Le fonctionnement général est le suivant :

.. code-block:: text

   Développeur
       |
       | git push
       v
   GitHub
       |
       v
   GitHub Actions
       |
       +--> Flake8
       |
       +--> collectstatic
       |
       +--> Pytest + coverage
       |
       v
   Build Docker
       |
       v
   Docker Hub
       |
       v
   Render
       |
       v
   Application en production

L'objectif est de vérifier automatiquement la qualité du projet avant de
construire et de déployer une nouvelle version.

Docker
------

L'application est conteneurisée avec Docker.

Le fichier ``Dockerfile`` définit l'environnement nécessaire à l'exécution
de l'application.

La configuration utilisée est la suivante :

.. code-block:: docker

   FROM python:3.9-slim-bookworm

   ENV PYTHONDONTWRITEBYTECODE=1
   ENV PYTHONUNBUFFERED=1

   WORKDIR /app

   COPY requirements.txt .

   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   RUN python manage.py collectstatic --noinput

   EXPOSE 8000

   CMD ["sh", "-c", "exec gunicorn oc_lettings_site.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2"]

Image de base
~~~~~~~~~~~~~

L'image utilise Python 3.9 sur une distribution Debian légère :

.. code-block:: text

   python:3.9-slim-bookworm

Cette image contient l'environnement Python nécessaire tout en limitant la
taille du conteneur.

Variables Python
~~~~~~~~~~~~~~~~

Les variables suivantes sont définies :

.. code-block:: docker

   ENV PYTHONDONTWRITEBYTECODE=1
   ENV PYTHONUNBUFFERED=1

``PYTHONDONTWRITEBYTECODE`` évite la génération de fichiers ``.pyc``.

``PYTHONUNBUFFERED`` permet d'envoyer immédiatement les logs vers la sortie
standard, ce qui est utile dans un environnement Docker.

Répertoire de travail
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: docker

   WORKDIR /app

Le dossier ``/app`` devient le répertoire de travail principal à l'intérieur
du conteneur.

Installation des dépendances
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Les dépendances sont installées à partir du fichier ``requirements.txt`` :

.. code-block:: docker

   COPY requirements.txt .

   RUN pip install --no-cache-dir -r requirements.txt

Le fichier des dépendances est copié avant le reste du projet afin de profiter
du système de cache des couches Docker.

Copie du projet
~~~~~~~~~~~~~~~

.. code-block:: docker

   COPY . .

Cette instruction copie le contenu du projet dans le conteneur.

Le fichier ``.dockerignore`` permet d'exclure les fichiers qui ne doivent pas
être intégrés à l'image, notamment les fichiers locaux ou sensibles.

Fichiers statiques
~~~~~~~~~~~~~~~~~~

Les fichiers statiques sont collectés pendant la construction de l'image :

.. code-block:: docker

   RUN python manage.py collectstatic --noinput

Ils sont ensuite servis en production grâce à WhiteNoise.

Serveur de production
~~~~~~~~~~~~~~~~~~~~~

L'application est exécutée avec Gunicorn :

.. code-block:: docker

   CMD ["sh", "-c", "exec gunicorn oc_lettings_site.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2"]

Gunicorn charge l'application WSGI Django depuis :

.. code-block:: text

   oc_lettings_site.wsgi:application

``0.0.0.0`` permet au serveur d'écouter sur toutes les interfaces réseau du
conteneur.

La variable :

.. code-block:: text

   ${PORT:-8000}

signifie que le port fourni par l'environnement est utilisé lorsqu'il existe.

Sinon, le port 8000 est utilisé par défaut.

Construire l'image localement
-----------------------------

Pour construire l'image Docker :

.. code-block:: bash

   docker build -t orange-county-lettings:local .

Pour lancer le conteneur :

.. code-block:: bash

   docker run --rm \
     -p 8000:8000 \
     --env-file .env \
     orange-county-lettings:local

L'application est alors accessible sur :

.. code-block:: text

   http://127.0.0.1:8000/

Docker Hub
----------

Les images de production sont publiées sur Docker Hub dans le dépôt :

.. code-block:: text

   tommouquet/orange-county-lettings

L'image la plus récente peut être téléchargée avec :

.. code-block:: bash

   docker pull tommouquet/orange-county-lettings:latest

Puis exécutée avec :

.. code-block:: bash

   docker run --rm \
     -p 8000:8000 \
     --env-file .env \
     tommouquet/orange-county-lettings:latest

Tags Docker
~~~~~~~~~~~

Chaque image générée depuis la branche ``master`` est publiée avec deux tags.

Le premier tag est :

.. code-block:: text

   latest

Il correspond à la version la plus récemment publiée.

Le second utilise le SHA du commit Git :

.. code-block:: text

   tommouquet/orange-county-lettings:<SHA_COMMIT>

Ce second tag permet d'identifier précisément la version du code utilisée
pour construire une image.

GitHub Actions
--------------

Le pipeline CI/CD est défini dans :

.. code-block:: text

   .github/workflows/ci.yml

Il contient trois jobs principaux :

.. code-block:: text

   tests
      |
      v
   docker
      |
      v
   deploy

Tests et qualité
~~~~~~~~~~~~~~~~

Le premier job exécute les contrôles de qualité du projet sur une machine
Ubuntu temporaire fournie par GitHub.

Il réalise notamment :

.. code-block:: text

   installation des dépendances
           |
           v
        Flake8
           |
           v
      collectstatic
           |
           v
   Pytest + coverage

La couverture minimale exigée est de 80 %.

La commande utilisée pour les tests est :

.. code-block:: bash

   pytest --cov=. --cov-report=term-missing --cov-fail-under=80

Si un test échoue, les jobs suivants ne sont pas exécutés.

Construction et publication Docker
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Le job Docker dépend du succès du job de tests.

Il est exécuté uniquement pour un push sur la branche ``master``.

Il construit l'image Docker puis la publie sur Docker Hub avec les tags :

.. code-block:: text

   latest
   SHA du commit

L'authentification à Docker Hub utilise des variables et secrets GitHub afin
de ne pas stocker les identifiants directement dans le fichier de workflow.

Déploiement
~~~~~~~~~~~

Le job de déploiement dépend du succès du job Docker.

Il est lui aussi exécuté uniquement lors d'un push sur ``master``.

Une requête HTTP est envoyée au Deploy Hook de Render :

.. code-block:: bash

   curl --fail --show-error --silent \
     --request POST \
     "${RENDER_DEPLOY_HOOK_URL}"

Render récupère alors la nouvelle image disponible sur Docker Hub et redémarre
le service avec cette version.

Branches
--------

Le pipeline est conçu pour distinguer les branches de développement de la
branche de production.

Pour un push sur une autre branche que ``master`` :

.. code-block:: text

   push
    |
    v
   tests
    |
    +--> fin

Pour un push sur ``master`` :

.. code-block:: text

   push
    |
    v
   tests
    |
    v
   Docker build + push
    |
    v
   Render deploy

Une branche secondaire peut donc être vérifiée par la CI sans provoquer de
déploiement en production.

Variables et secrets
--------------------

Les données sensibles ne sont pas enregistrées directement dans le dépôt Git.

GitHub Actions utilise notamment :

.. code-block:: text

   DOCKERHUB_USERNAME
   DOCKERHUB_TOKEN
   RENDER_DEPLOY_HOOK_URL

Render dispose également de ses propres variables d'environnement pour
configurer Django en production.

Les principales variables sont :

.. code-block:: text

   SECRET_KEY
   DEBUG
   ALLOWED_HOSTS
   SENTRY_DSN
   SENTRY_ENVIRONMENT

En production, ``DEBUG`` doit être désactivé.

Par exemple :

.. code-block:: text

   DEBUG=False

``ALLOWED_HOSTS`` doit contenir le domaine utilisé par l'application.

Render
------

Render exécute l'image Docker publiée sur Docker Hub.

L'application en production est disponible à l'adresse :

.. code-block:: text

   https://orange-county-lettings-a4ee.onrender.com/

Render fournit une variable ``PORT`` à l'application.

Le Dockerfile utilise cette valeur automatiquement grâce à :

.. code-block:: text

   ${PORT:-8000}

Cela permet d'utiliser la même image aussi bien localement que sur Render.

Fichiers statiques
------------------

Les fichiers CSS, JavaScript et autres ressources statiques sont préparés avec
la commande :

.. code-block:: bash

   python manage.py collectstatic --noinput

En production, WhiteNoise permet à l'application Django de servir ces fichiers
sans dépendre d'un serveur statique externe.

Base SQLite en production
-------------------------

Le projet utilise SQLite.

Cette solution est suffisante pour l'application de démonstration Orange
County Lettings.

Cependant, le système de fichiers d'un conteneur peut être éphémère sur une
plateforme d'hébergement.

Pour une application réelle nécessitant des écritures persistantes et une
utilisation plus importante, une base externe telle que PostgreSQL serait
plus adaptée.

Retour à une version précédente
-------------------------------

Lorsqu'un commit déjà publié doit être annulé, il est possible d'utiliser :

.. code-block:: bash

   git revert <SHA_COMMIT>

Cette commande crée un nouveau commit qui inverse les modifications du commit
ciblé.

Après un nouveau ``git push`` sur ``master``, le pipeline est relancé et cette
nouvelle version peut être reconstruite et redéployée.

Cela permet de conserver l'historique Git sans réécrire les commits déjà
publiés.