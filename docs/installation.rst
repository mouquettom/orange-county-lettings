Installation et démarrage rapide
================================

Prérequis
---------

Le projet utilise Python 3.9 et Django 3.0.

Avant de commencer, vérifier que les outils suivants sont disponibles :

- Python 3.9
- Git
- pip
- un environnement virtuel Python

Cloner le projet
----------------

Cloner le dépôt GitHub :

.. code-block:: bash

   git clone https://github.com/mouquettom/orange-county-lettings.git
   cd orange-county-lettings

Créer un environnement virtuel
-------------------------------

Sous macOS ou Linux :

.. code-block:: bash

   python3 -m venv .venv
   source .venv/bin/activate

Sous Windows :

.. code-block:: powershell

   python -m venv .venv
   .venv\Scripts\activate

Installer les dépendances
-------------------------

Mettre pip à jour puis installer les dépendances du projet :

.. code-block:: bash

   python -m pip install --upgrade pip
   pip install -r requirements.txt

Configurer les variables d'environnement
----------------------------------------

Créer un fichier ``.env`` à la racine du projet.

Exemple de configuration pour l'environnement de développement :

.. code-block:: text

   SECRET_KEY=change-me-for-local-development
   DEBUG=True
   ALLOWED_HOSTS=127.0.0.1,localhost

   SENTRY_DSN=
   SENTRY_ENVIRONMENT=development

Le fichier ``.env`` contient des informations de configuration potentiellement
sensibles et ne doit pas être versionné dans Git.

Le fichier ``.env.example`` peut être utilisé comme modèle afin de connaître
les variables nécessaires sans exposer de secret.

Appliquer les migrations
------------------------

Appliquer les migrations Django à la base de données :

.. code-block:: bash

   python manage.py migrate

Lancer le serveur de développement
----------------------------------

Démarrer l'application avec le serveur de développement Django :

.. code-block:: bash

   python manage.py runserver

L'application est ensuite accessible à l'adresse :

.. code-block:: text

   http://127.0.0.1:8000/

L'interface d'administration Django est accessible à l'adresse :

.. code-block:: text

   http://127.0.0.1:8000/admin/

Démarrage rapide
----------------

Pour démarrer rapidement le projet après l'avoir cloné :

.. code-block:: bash

   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver

Le projet utilise SQLite comme base de données locale. Aucune installation
d'un serveur de base de données externe n'est donc nécessaire pour lancer
l'application dans son environnement de développement.