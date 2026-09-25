Architecture du projet
======================

Vue d'ensemble
--------------

Orange County Lettings est une application web développée avec Django.

Le projet a été refactorisé afin de séparer les différentes responsabilités
fonctionnelles dans plusieurs applications Django.

L'architecture principale repose sur trois modules :

- ``oc_lettings_site`` : configuration générale du projet ;
- ``lettings`` : gestion des locations et des adresses ;
- ``profiles`` : gestion des profils utilisateurs.

Cette séparation permet de rendre le code plus lisible, maintenable et
évolutif.

Structure générale
------------------

L'organisation simplifiée du projet est la suivante :

.. code-block:: text

   orange-county-lettings/
   ├── .github/
   │   └── workflows/
   │       └── ci.yml
   │
   ├── lettings/
   │   ├── migrations/
   │   ├── templates/
   │   │   └── lettings/
   │   ├── tests/
   │   ├── models.py
   │   ├── urls.py
   │   └── views.py
   │
   ├── profiles/
   │   ├── migrations/
   │   ├── templates/
   │   │   └── profiles/
   │   ├── tests/
   │   ├── models.py
   │   ├── urls.py
   │   └── views.py
   │
   ├── oc_lettings_site/
   │   ├── tests/
   │   ├── settings.py
   │   ├── urls.py
   │   ├── views.py
   │   └── wsgi.py
   │
   ├── docs/
   ├── static/
   ├── templates/
   ├── Dockerfile
   ├── manage.py
   ├── requirements.txt
   ├── setup.cfg
   └── oc-lettings-site.sqlite3

Application ``oc_lettings_site``
--------------------------------

Le module ``oc_lettings_site`` contient la configuration générale du projet
Django.

Il regroupe notamment :

- les paramètres dans ``settings.py`` ;
- les URLs principales dans ``urls.py`` ;
- la page d'accueil ;
- les handlers personnalisés pour les erreurs HTTP 404 et 500 ;
- la configuration WSGI utilisée par Gunicorn en production.

Il constitue le point d'entrée principal du projet mais ne contient plus la
logique métier des locations ou des profils.

Application ``lettings``
-------------------------

L'application ``lettings`` regroupe tout ce qui concerne les locations
immobilières.

Elle contient notamment les modèles :

- ``Address`` ;
- ``Letting``.

Elle gère :

- l'affichage de la liste des locations ;
- l'affichage du détail d'une location ;
- les adresses associées aux locations ;
- les URLs, vues, templates et tests propres à cette fonctionnalité.

Application ``profiles``
-------------------------

L'application ``profiles`` regroupe les fonctionnalités liées aux profils
utilisateurs.

Elle contient le modèle ``Profile``.

Elle gère :

- l'affichage de la liste des profils ;
- l'affichage du détail d'un profil ;
- les URLs, vues, templates et tests propres aux profils.

Séparation des responsabilités
------------------------------

Avant la refactorisation, plusieurs fonctionnalités étaient regroupées dans
le même module Django.

La séparation en applications permet d'obtenir une organisation plus claire :

.. code-block:: text

   oc_lettings_site
       └── configuration générale

   lettings
       └── locations et adresses

   profiles
       └── profils utilisateurs

Chaque application contient ses propres composants :

.. code-block:: text

   modèles
      ↓
   vues
      ↓
   URLs
      ↓
   templates
      ↓
   tests

Cycle d'une requête Django
--------------------------

Lorsqu'un utilisateur consulte une page, la requête traverse plusieurs
composants Django.

Exemple simplifié :

.. code-block:: text

   Navigateur
       ↓
   URL Django
       ↓
   Vue
       ↓
   Modèle / base de données
       ↓
   Vue
       ↓
   Template
       ↓
   Réponse HTML
       ↓
   Navigateur

Par exemple, lors de la consultation d'une location :

1. Django recherche l'URL correspondante dans ``lettings/urls.py`` ;
2. la vue associée dans ``lettings/views.py`` est appelée ;
3. la vue récupère les données nécessaires via les modèles ;
4. les données sont transmises au template ;
5. Django génère la réponse HTML envoyée au navigateur.

Technologies utilisées
----------------------

Back-end
~~~~~~~~

- Python 3.9
- Django 3.0
- SQLite3

Tests et qualité
~~~~~~~~~~~~~~~~

- Pytest
- pytest-django
- pytest-cov
- Coverage
- Flake8

Observabilité
~~~~~~~~~~~~~

- Python ``logging``
- Sentry

Production
~~~~~~~~~~

- Gunicorn
- WhiteNoise
- Docker

CI/CD et hébergement
~~~~~~~~~~~~~~~~~~~~

- GitHub Actions
- Docker Hub
- Render

Documentation
~~~~~~~~~~~~~

- Sphinx
- sphinx-rtd-theme
- Read the Docs