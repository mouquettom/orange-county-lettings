Project Architecture
====================

Overview
--------

Orange County Lettings is a web application built with Django.

The project was refactored to split its functional responsibilities across
several Django applications.

The main architecture relies on three modules:

- ``oc_lettings_site``: general project configuration;
- ``lettings``: management of lettings and addresses;
- ``profiles``: management of user profiles.

This separation makes the code more readable, maintainable and scalable.

General structure
-----------------

The simplified project layout is as follows:

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
   ├── requirements-dev.txt
   ├── setup.cfg
   └── oc-lettings-site.sqlite3

``oc_lettings_site`` application
--------------------------------

The ``oc_lettings_site`` module contains the general configuration of the
Django project.

It includes, among other things:

- the settings in ``settings.py``;
- the root URLs in ``urls.py``;
- the home page;
- the custom handlers for HTTP 404 and 500 errors;
- the WSGI configuration used by Gunicorn in production.

It is the main entry point of the project but no longer contains the business
logic for lettings or profiles.

``lettings`` application
------------------------

The ``lettings`` application groups everything related to property lettings.

It contains the following models:

- ``Address``;
- ``Letting``.

It handles:

- displaying the list of lettings;
- displaying the details of a letting;
- the addresses associated with lettings;
- the URLs, views, templates and tests specific to this feature.

``profiles`` application
------------------------

The ``profiles`` application groups the features related to user profiles.

It contains the ``Profile`` model.

It handles:

- displaying the list of profiles;
- displaying the details of a profile;
- the URLs, views, templates and tests specific to profiles.

Separation of responsibilities
------------------------------

Before the refactoring, several features were grouped in the same Django
module.

Splitting them into applications gives a clearer organization:

.. code-block:: text

   oc_lettings_site
       └── general configuration

   lettings
       └── lettings and addresses

   profiles
       └── user profiles

Each application contains its own components:

.. code-block:: text

   models
      ↓
   views
      ↓
   URLs
      ↓
   templates
      ↓
   tests

Django request lifecycle
------------------------

When a user visits a page, the request goes through several Django components.

Simplified example:

.. code-block:: text

   Browser
       ↓
   Django URL
       ↓
   View
       ↓
   Model / database
       ↓
   View
       ↓
   Template
       ↓
   HTML response
       ↓
   Browser

For example, when viewing a letting:

1. Django looks up the matching URL in ``lettings/urls.py``;
2. the associated view in ``lettings/views.py`` is called;
3. the view retrieves the required data through the models;
4. the data is passed to the template;
5. Django generates the HTML response sent to the browser.

Technologies
------------

Back-end
~~~~~~~~

- Python 3.9
- Django 3.0
- SQLite3

Testing and code quality
~~~~~~~~~~~~~~~~~~~~~~~~

- Pytest
- pytest-django
- pytest-cov
- Coverage
- Flake8

Observability
~~~~~~~~~~~~~

- Python ``logging``
- Sentry

Production
~~~~~~~~~~

- Gunicorn
- WhiteNoise
- Docker

CI/CD and hosting
~~~~~~~~~~~~~~~~~

- GitHub Actions
- Docker Hub
- Render

Documentation
~~~~~~~~~~~~~

- Sphinx
- sphinx-rtd-theme
- Read the Docs
