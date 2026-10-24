Installation and Quick Start
============================

Requirements
------------

The project uses Python 3.9 and Django 3.0.

Before starting, make sure the following tools are available:

- Python 3.9
- Git
- pip

Check that Python 3.9 is available:

.. code-block:: bash

   python3.9 --version

.. note::

   Explicitly use Python 3.9 to create the virtual environment. A generic
   command such as ``python3 -m venv .venv`` may use a newer Python version
   installed on your machine, which is not compatible with Django 3.0.

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

   python3.9 -m venv .venv
   source .venv/bin/activate

On Windows, using the Python launcher:

.. code-block:: powershell

   py -3.9 -m venv .venv
   .venv\Scripts\activate

Check the Python version used by the virtual environment:

.. code-block:: bash

   python --version

The expected result is ``Python 3.9.x``.

Install dependencies
--------------------

Upgrade pip, then install the project dependencies:

.. code-block:: bash

   python -m pip install --upgrade pip
   pip install -r requirements-dev.txt

``requirements-dev.txt`` includes the runtime dependencies listed in
``requirements.txt`` plus the testing and linting tools.

Configure environment variables
-------------------------------

Create a ``.env`` file at the root of the project from the provided example:

.. code-block:: bash

   cp .env.example .env

On Windows:

.. code-block:: powershell

   copy .env.example .env

Generate a Django secret key:

.. code-block:: bash

   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

Copy the generated value into ``.env``. Example configuration for the
development environment:

.. code-block:: text

   SECRET_KEY=<generated-key>
   DEBUG=True
   ALLOWED_HOSTS=127.0.0.1,localhost

   SENTRY_DSN=
   SENTRY_ENVIRONMENT=development

Debug mode is disabled unless ``DEBUG=True`` is set. When it is disabled, the
application refuses to start without a ``SECRET_KEY``. With ``DEBUG=True``, a
development-only key is used if ``SECRET_KEY`` is left empty.

``SENTRY_DSN`` can remain empty to run the application without Sentry.

The ``.env`` file contains potentially sensitive configuration and must not be
committed to Git.

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

To quickly start the project on macOS or Linux after cloning it:

.. code-block:: bash

   python3.9 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements-dev.txt
   cp .env.example .env
   python manage.py migrate
   python manage.py runserver

The project uses SQLite as its local database, so no external database server
needs to be installed to run the application in development.
