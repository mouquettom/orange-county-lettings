Installation and Quick Start
============================

Requirements
------------

The project uses Python 3.9 and Django 3.0.

Before starting, make sure the following tools are available:

- Python 3.9
- Git
- pip
- a Python virtual environment

Clone the project
-----------------

Clone the GitHub repository:

.. code-block:: bash

   git clone https://github.com/mouquettom/orange-county-lettings.git
   cd orange-county-lettings

Create a virtual environment
----------------------------

On macOS or Linux:

.. code-block:: bash

   python3 -m venv .venv
   source .venv/bin/activate

On Windows:

.. code-block:: powershell

   python -m venv .venv
   .venv\Scripts\activate

Install dependencies
--------------------

Upgrade pip, then install the project dependencies:

.. code-block:: bash

   python -m pip install --upgrade pip
   pip install -r requirements-dev.txt

Configure environment variables
-------------------------------

Create a ``.env`` file at the root of the project.

Example configuration for the development environment:

.. code-block:: text

   SECRET_KEY=change-me-for-local-development
   DEBUG=True
   ALLOWED_HOSTS=127.0.0.1,localhost

   SENTRY_DSN=
   SENTRY_ENVIRONMENT=development

The ``.env`` file contains potentially sensitive configuration and must not be
committed to Git.

The ``.env.example`` file can be used as a template to see which variables are
required without exposing any secret.

Apply migrations
----------------

Apply the Django migrations to the database:

.. code-block:: bash

   python manage.py migrate

Run the development server
--------------------------

Start the application with the Django development server:

.. code-block:: bash

   python manage.py runserver

The application is then available at:

.. code-block:: text

   http://127.0.0.1:8000/

The Django administration interface is available at:

.. code-block:: text

   http://127.0.0.1:8000/admin/

Quick start
-----------

To quickly start the project after cloning it:

.. code-block:: bash

   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements-dev.txt
   python manage.py migrate
   python manage.py runserver

The project uses SQLite as its local database, so no external database server
needs to be installed to run the application in development.