Deployment and CI/CD
====================

Overview
--------

Orange County Lettings uses an automated deployment pipeline based on Docker,
GitHub Actions, Docker Hub and Render.

The overall flow is as follows:

.. code-block:: text

   Developer
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
   Docker build
       |
       v
   Docker Hub
       |
       v
   Render
       |
       v
   Production application

The goal is to automatically check the quality of the project before building
and deploying a new version.

Docker
------

The application is containerized with Docker.

The ``Dockerfile`` defines the environment required to run the application.

The configuration used is the following:

.. code-block:: docker

   FROM python:3.9-slim-bookworm

   ENV PYTHONDONTWRITEBYTECODE=1
   ENV PYTHONUNBUFFERED=1

   WORKDIR /app

   COPY requirements.txt .

   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   RUN SECRET_KEY=build-only-collectstatic python manage.py collectstatic --noinput

   EXPOSE 8000

   CMD ["sh", "-c", "exec gunicorn oc_lettings_site.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2"]

Base image
~~~~~~~~~~

The image uses Python 3.9 on a lightweight Debian distribution:

.. code-block:: text

   python:3.9-slim-bookworm

This image provides the required Python environment while keeping the
container small.

Python variables
~~~~~~~~~~~~~~~~

The following variables are defined:

.. code-block:: docker

   ENV PYTHONDONTWRITEBYTECODE=1
   ENV PYTHONUNBUFFERED=1

``PYTHONDONTWRITEBYTECODE`` prevents ``.pyc`` files from being generated.

``PYTHONUNBUFFERED`` sends logs to standard output immediately, which is useful
in a Docker environment.

Working directory
~~~~~~~~~~~~~~~~~

.. code-block:: docker

   WORKDIR /app

The ``/app`` folder becomes the main working directory inside the container.

Installing dependencies
~~~~~~~~~~~~~~~~~~~~~~~

Dependencies are installed from the ``requirements.txt`` file:

.. code-block:: docker

   COPY requirements.txt .

   RUN pip install --no-cache-dir -r requirements.txt

The requirements file is copied before the rest of the project to take
advantage of Docker layer caching.

Copying the project
~~~~~~~~~~~~~~~~~~~

.. code-block:: docker

   COPY . .

This instruction copies the project content into the container.

The ``.dockerignore`` file excludes files that must not be included in the
image, such as local or sensitive files.

Static files
~~~~~~~~~~~~

Static files are collected while the image is built:

.. code-block:: docker

   RUN SECRET_KEY=build-only-collectstatic python manage.py collectstatic --noinput

``collectstatic`` loads the Django settings, which require a ``SECRET_KEY``
because debug mode is disabled by default. The build-only value is set for
this command only and is not stored in the image: the real key is provided at
runtime by Render.

The collected files are then served in production by WhiteNoise.

Production server
~~~~~~~~~~~~~~~~~

The application runs with Gunicorn:

.. code-block:: docker

   CMD ["sh", "-c", "exec gunicorn oc_lettings_site.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2"]

Gunicorn loads the Django WSGI application from:

.. code-block:: text

   oc_lettings_site.wsgi:application

``0.0.0.0`` makes the server listen on every network interface of the
container.

The variable:

.. code-block:: text

   ${PORT:-8000}

means that the port provided by the environment is used when it exists.

Otherwise, port 8000 is used by default.

Build the image locally
-----------------------

To build the Docker image:

.. code-block:: bash

   docker build -t orange-county-lettings:local .

To run the container:

.. code-block:: bash

   docker run --rm \
     -p 8000:8000 \
     --env-file .env \
     orange-county-lettings:local

The application is then available at:

.. code-block:: text

   http://127.0.0.1:8000/

Docker Hub
----------

Production images are published on Docker Hub in the repository:

.. code-block:: text

   tommouquet/orange-county-lettings

The latest image can be pulled with:

.. code-block:: bash

   docker pull tommouquet/orange-county-lettings:latest

Then run with:

.. code-block:: bash

   docker run --rm \
     -p 8000:8000 \
     --env-file .env \
     tommouquet/orange-county-lettings:latest

Docker tags
~~~~~~~~~~~

Each image built from the ``master`` branch is published with two tags.

The first tag is:

.. code-block:: text

   latest

It points to the most recently published version.

The second one uses the Git commit SHA:

.. code-block:: text

   tommouquet/orange-county-lettings:<COMMIT_SHA>

This second tag identifies exactly which version of the code was used to build
an image.

GitHub Actions
--------------

The CI/CD pipeline is defined in:

.. code-block:: text

   .github/workflows/ci.yml

It contains three main jobs:

.. code-block:: text

   tests
      |
      v
   docker
      |
      v
   deploy

Tests and code quality
~~~~~~~~~~~~~~~~~~~~~~

The first job runs the project's quality checks on a temporary Ubuntu machine
provided by GitHub.

It performs, among other things:

.. code-block:: text

   dependency installation
           |
           v
        Flake8
           |
           v
      collectstatic
           |
           v
   Pytest + coverage

The minimum required coverage is 80%.

The job defines a throwaway ``SECRET_KEY`` environment variable, used only to
run these checks.

The command used to run the tests is:

.. code-block:: bash

   pytest --cov=. --cov-report=term-missing --cov-fail-under=80

If a test fails, the following jobs are not run.

Docker build and publication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Docker job depends on the success of the tests job.

It only runs on a push to the ``master`` branch.

It builds the Docker image and publishes it to Docker Hub with the tags:

.. code-block:: text

   latest
   commit SHA

Docker Hub authentication uses GitHub variables and secrets so that
credentials are not stored directly in the workflow file.

Deployment
~~~~~~~~~~

The deployment job depends on the success of the Docker job.

It also only runs on a push to ``master``.

An HTTP request is sent to the Render Deploy Hook:

.. code-block:: bash

   curl --fail --show-error --silent \
     --request POST \
     "${RENDER_DEPLOY_HOOK_URL}"

Render then pulls the new image from Docker Hub and restarts the service with
this version.

Branches
--------

The pipeline is designed to distinguish development branches from the
production branch.

For a push to a branch other than ``master``:

.. code-block:: text

   push
    |
    v
   tests
    |
    +--> end

For a push to ``master``:

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

A secondary branch can therefore be checked by the CI without triggering a
production deployment.

Variables and secrets
---------------------

Sensitive data is not stored directly in the Git repository.

GitHub Actions notably uses:

.. code-block:: text

   DOCKERHUB_USERNAME
   DOCKERHUB_TOKEN
   RENDER_DEPLOY_HOOK_URL

Render also has its own environment variables to configure Django in
production.

The main variables are:

.. code-block:: text

   SECRET_KEY
   DEBUG
   ALLOWED_HOSTS
   SENTRY_DSN
   SENTRY_ENVIRONMENT

In production, ``DEBUG`` must be disabled.

For example:

.. code-block:: text

   DEBUG=False

Debug mode is disabled unless ``DEBUG=True`` is explicitly set. When it is
disabled, the application refuses to start without a ``SECRET_KEY``, so a
missing production key cannot go unnoticed.

``ALLOWED_HOSTS`` must contain the domain used by the application.

Render
------

Render runs the Docker image published on Docker Hub.

The production application is available at:

.. code-block:: text

   https://orange-county-lettings-a4ee.onrender.com/

Render provides a ``PORT`` variable to the application.

The Dockerfile uses this value automatically thanks to:

.. code-block:: text

   ${PORT:-8000}

This makes it possible to use the same image both locally and on Render.

Static files
------------

CSS, JavaScript and other static resources are prepared with the command:

.. code-block:: bash

   python manage.py collectstatic --noinput

In production, WhiteNoise lets the Django application serve these files without
relying on an external static file server.

SQLite in production
--------------------

The project uses SQLite.

This is sufficient for the Orange County Lettings demonstration application.

However, a container's file system can be ephemeral on a hosting platform.

For a real application that needs persistent writes and heavier usage, an
external database such as PostgreSQL would be more suitable.

Rolling back to a previous version
----------------------------------

When a commit that has already been pushed must be undone, you can use:

.. code-block:: bash

   git revert <COMMIT_SHA>

This command creates a new commit that reverses the changes of the targeted
commit.

After a new ``git push`` to ``master``, the pipeline runs again and this new
version can be rebuilt and redeployed.

This keeps the Git history intact without rewriting commits that have already
been published.

Maintenance and day-to-day operations
-------------------------------------

Before publishing a significant change, it is recommended to run the project's
quality checks locally.

Check linting:

.. code-block:: bash

   flake8 oc_lettings_site lettings profiles manage.py

Run the tests and check coverage:

.. code-block:: bash

   pytest --cov=. --cov-report=term-missing --cov-fail-under=80

Rebuild the Sphinx documentation:

.. code-block:: bash

   cd docs
   make html

Application errors in production can be reviewed in Sentry.

The container's runtime logs can also be viewed from the Render dashboard.

The application data can be managed through the Django administration
interface available at:

.. code-block:: text

   /admin/

When a change is pushed to the ``master`` branch, GitHub Actions automatically
checks the project before building and deploying a new version.