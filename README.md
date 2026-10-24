# Orange County Lettings

Django web application for managing property lettings and user profiles, refactored and industrialized as part of the **OpenClassrooms Python Application Developer** program.

This project implements:

- a modular Django architecture;
- automated testing with Pytest;
- test coverage above 80%;
- code quality checks with Flake8;
- Python logging and exception monitoring with Sentry;
- Docker containerization;
- a CI/CD pipeline with GitHub Actions;
- automatic image publishing to Docker Hub;
- automatic deployment to Render;
- technical documentation generated with Sphinx and published on Read the Docs.

---

## Table of Contents

- [Overview](#overview)
- [Production Application](#production-application)
- [Technologies](#technologies)
- [Project Architecture](#project-architecture)
- [Database](#database)
- [Local Installation](#local-installation)
- [Environment Variables](#environment-variables)
- [Run the Application](#run-the-application)
- [Tests and Code Quality](#tests-and-code-quality)
- [Logging and Sentry](#logging-and-sentry)
- [Docker](#docker)
- [CI/CD](#cicd)
- [Deployment](#deployment)
- [Technical Documentation](#technical-documentation)
- [Useful Commands](#useful-commands)
- [Security](#security)

---

## Overview

Orange County Lettings allows users to browse:

- the list of lettings;
- the details of a letting and its address;
- the list of user profiles;
- the details of a user profile;
- the Django administration interface.

The application was refactored to separate responsibilities into several Django applications:

- `oc_lettings_site`: general project configuration and global pages;
- `lettings`: letting and address management;
- `profiles`: user profile management.

Custom **404** and **500** error pages are also implemented.

---

## Production Application

Public application:

https://orange-county-lettings-a4ee.onrender.com/

Technical documentation:

https://orange-county-lettings-read-the-docs.readthedocs.io/en/latest/

GitHub repository:

https://github.com/mouquettom/orange-county-lettings

GitHub Actions pipeline:

https://github.com/mouquettom/orange-county-lettings/actions

Public Docker image:

```text
tommouquet/orange-county-lettings
```

The latest image can be pulled with:

```bash
docker pull tommouquet/orange-county-lettings:latest
```

Each build produced from `master` is also published with a tag matching the **Git commit SHA**.

---

## Technologies

### Back-end

- Python **3.9**
- Django 3.0
- SQLite3
- Gunicorn

> **Important:** this project must be run with **Python 3.9**.  
> Recent Python versions, especially Python 3.12 and above, are not suitable for this historical Django version. For example, `distutils`, used by Django 3.0, is no longer available by default in recent Python versions.

### Testing and code quality

- Pytest
- pytest-django
- pytest-cov
- Coverage
- Flake8

### Production and observability

- Sentry
- Python `logging`
- WhiteNoise
- python-dotenv

### DevOps

- Docker
- Docker Hub
- GitHub Actions
- Render

### Documentation

- Sphinx
- sphinx-rtd-theme
- Read the Docs
- Autodoc

---

## Project Architecture

Simplified structure:

```text
orange-county-lettings/
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── docs/
│   ├── conf.py
│   ├── index.rst
│   ├── installation.rst
│   ├── architecture.rst
│   ├── models.rst
│   ├── usage.rst
│   ├── deployment.rst
│   ├── api.rst
│   └── requirements.txt
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
├── static/
├── templates/
├── Dockerfile
├── manage.py
├── requirements.txt
├── requirements-dev.txt
├── setup.cfg
├── .env.example
├── .readthedocs.yaml
└── oc-lettings-site.sqlite3
```

### `lettings` application

This application contains the following models:

- `Address`
- `Letting`

It handles:

- the letting list;
- letting details;
- addresses associated with lettings.

### `profiles` application

This application contains the following model:

- `Profile`

It handles:

- the profile list;
- user profile details.

### `oc_lettings_site` application

This application contains, among other things:

- the home page;
- the main Django configuration;
- custom 404 and 500 handlers;
- root project URLs.

---

## Database

The project uses **SQLite3**.

### `Address` model

An address contains:

- a street number;
- a street name;
- a city;
- a state;
- a ZIP code;
- an ISO country code.

### `Letting` model

A letting contains:

- a title;
- a `OneToOne` relationship with an `Address`.

### `Profile` model

A profile contains:

- a `OneToOne` relationship with Django's `User` model;
- an optional favorite city.

Simplified schema:

```text
User
  │
  └── 1 — 1 ── Profile

Letting
  │
  └── 1 — 1 ── Address
```

During the refactoring process, the data from the original application was preserved using **Django data migrations**. The new tables were created first, then the data was copied while preserving IDs and relationships, and finally the old models were removed.

---

# Local Installation

## Requirements

- Git
- **Python 3.9**
- `pip`
- Docker Desktop only if you want to test containerization

Check that Python 3.9 is available:

```bash
python3.9 --version
```

Expected result:

```text
Python 3.9.x
```

> Explicitly use Python 3.9 to create the virtual environment.  
> A generic command such as `python3 -m venv .venv` may use a newer Python version installed on your machine and make Django 3.0 incompatible.

## 1. Clone the repository

```bash
git clone https://github.com/mouquettom/orange-county-lettings.git
cd orange-county-lettings
```

## 2. Create a virtual environment with Python 3.9

### macOS / Linux

```bash
python3.9 -m venv .venv
source .venv/bin/activate
```

### Windows

Using the Python launcher:

```bash
py -3.9 -m venv .venv
.venv\Scripts\activate
```

Check the Python version actually used by the virtual environment:

```bash
python --version
```

Expected result:

```text
Python 3.9.x
```

## 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

Dependencies are split into two files:

- `requirements.txt`: runtime dependencies only, installed in the Docker image;
- `requirements-dev.txt`: runtime dependencies plus the testing and linting tools (Pytest, Coverage, Flake8), used locally and in the CI.

## 4. Configure environment variables

Create `.env` from the provided example file.

### macOS / Linux

```bash
cp .env.example .env
```

### Windows

```cmd
copy .env.example .env
```

### Generate a Django `SECRET_KEY`

After installing dependencies, generate a random Django secret key with:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the generated value into `.env`.

Example local configuration:

```env
SECRET_KEY=<generated-key>
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

SENTRY_DSN=
SENTRY_ENVIRONMENT=development
```

`SENTRY_DSN` may remain empty for local use without Sentry.

The `.env` file must never be committed to Git.

## 5. Check the Django configuration

```bash
python manage.py check
```

Expected result:

```text
System check identified no issues
```

## 6. Apply migrations

```bash
python manage.py migrate
```

You can also display migration status with:

```bash
python manage.py showmigrations
```

To check that no model change is waiting for a new migration:

```bash
python manage.py makemigrations --check --dry-run
```

---

## Environment Variables

The main environment variables used by the application are:

| Variable | Description | Default | Local example |
|---|---|---|---|
| `SECRET_KEY` | Django secret key | required when `DEBUG` is not `True` | locally generated key |
| `DEBUG` | Enables or disables debug mode | `False` | `True` |
| `ALLOWED_HOSTS` | Allowed hosts, separated by commas | `127.0.0.1,localhost` | `127.0.0.1,localhost` |
| `SENTRY_DSN` | Sentry project DSN | empty (Sentry disabled) | empty if Sentry is not used |
| `SENTRY_ENVIRONMENT` | Sentry environment name | `development` | `development` |

Debug mode is disabled unless `DEBUG=True` is explicitly set. When debug mode is disabled, the application refuses to start without a `SECRET_KEY`, so a missing production key cannot go unnoticed. In local development with `DEBUG=True`, a development-only key is used if `SECRET_KEY` is left empty.

Production example:

```env
SECRET_KEY=<production-key>
DEBUG=False
ALLOWED_HOSTS=orange-county-lettings-a4ee.onrender.com
SENTRY_DSN=<Sentry-DSN>
SENTRY_ENVIRONMENT=production
```

Production-specific values are configured directly in **Render** and are not stored in Git.

---

## Run the Application

### Django development server

```bash
python manage.py runserver
```

The application is then available at:

http://127.0.0.1:8000/

### Django administration

http://127.0.0.1:8000/admin/

---

## Tests and Code Quality

The project uses **Pytest** for automated testing and **Flake8** for code quality checks.

Tests are organized inside the corresponding applications:

```text
lettings/tests/
profiles/tests/
oc_lettings_site/tests/
```

They cover:

- models;
- URLs;
- views;
- templates;
- 404 responses;
- custom 404 and 500 handlers;
- application logging.

The current suite contains **18 tests**. The CI pipeline enforces a minimum test coverage of **80%**.

### Run Flake8

```bash
flake8 oc_lettings_site lettings profiles manage.py
```

No output means that no Flake8 issue was detected.

### Collect static files

```bash
python manage.py collectstatic --noinput
```

### Run tests

```bash
pytest
```

### Run tests with coverage

```bash
pytest --cov=. --cov-report=term-missing --cov-fail-under=80
```

If coverage falls below 80%, the command fails.

---

## Logging and Sentry

The application uses Python's standard `logging` module.

Logs are generated in:

- `lettings`;
- `profiles`;
- `oc_lettings_site`.

Each module may create its own logger with:

```python
logger = logging.getLogger(__name__)
```

`__name__` identifies the source module, for example `lettings.views`.

### Log levels used in this project

- `INFO`: normal application behavior;
- `WARNING`: unusual but handled situations.

Examples:

```text
INFO    → displaying the lettings list
WARNING → requested letting not found, followed by a 404 response
```

### Sentry

Sentry complements application logs by centralizing **exceptions**, especially unhandled exceptions.

Thanks to the Django integration, Sentry can provide:

- the exception type;
- the error message;
- the stack trace;
- the related file and line;
- the requested URL;
- the environment (`development` or `production`);
- technical context about the event.

Sentry therefore does not replace logs: both tools are complementary.

Local configuration:

```env
SENTRY_DSN=
SENTRY_ENVIRONMENT=development
```

Production configuration:

```env
SENTRY_DSN=<Sentry-DSN>
SENTRY_ENVIRONMENT=production
```

The DSN is not hard-coded in the source code.

---

## Docker

The project is fully containerized.

The `Dockerfile`:

- uses a lightweight **Python 3.9** image;
- installs dependencies;
- copies the project source code;
- runs `collectstatic`;
- exposes port 8000 for local use;
- starts the application with Gunicorn.

Gunicorn listens on:

```text
0.0.0.0:${PORT:-8000}
```

This allows:

- port `8000` to be used locally by default;
- the port provided automatically by Render to be used in production.

### Build the image locally

```bash
docker build -t orange-county-lettings:local .
```

### Run the local image

```bash
docker run --rm \
  -p 8000:8000 \
  --env-file .env \
  orange-county-lettings:local
```

Then open:

http://127.0.0.1:8000/

### Pull the image from Docker Hub

```bash
docker pull tommouquet/orange-county-lettings:latest
```

### Run the Docker Hub image

```bash
docker run --rm \
  -p 8000:8000 \
  --env-file .env \
  tommouquet/orange-county-lettings:latest
```

This second method verifies that the image published on Docker Hub works independently from a local build.

---

## CI/CD

The workflow is defined in:

```text
.github/workflows/ci.yml
```

### Push to any branch

On every push, GitHub Actions runs the quality job:

```text
Checkout
   ↓
Python 3.9
   ↓
Install dependencies
   ↓
Flake8
   ↓
collectstatic
   ↓
Pytest + Coverage >= 80%
```

Pull Requests targeting `master` also run these checks.

On a branch other than `master`, Docker publishing and Render deployment jobs are skipped.

### Push to `master`

When a push is made to `master`, the pipeline continues only if the tests succeed:

```text
Tests and code quality
          ↓
Build and push Docker image
          ↓
Deploy to Render
```

An invalid version therefore cannot be published or deployed if tests, Flake8, or coverage checks fail.

### Docker publishing

The pipeline publishes the same Docker image with two tags:

```text
tommouquet/orange-county-lettings:latest
tommouquet/orange-county-lettings:<COMMIT_SHA>
```

- `latest` points to the most recent image;
- the SHA tag identifies exactly which Docker image belongs to a given Git commit.

### GitHub Actions variables and secrets

In:

```text
Repository
→ Settings
→ Secrets and variables
→ Actions
```

Configure:

#### Repository variable

```text
DOCKERHUB_USERNAME
```

#### Repository secrets

```text
DOCKERHUB_TOKEN
RENDER_DEPLOY_HOOK_URL
```

These values are not written directly inside `ci.yml`.

---

## Deployment

The application is deployed on **Render** from the Docker image published on Docker Hub.

Architecture:

```text
Local code
    ↓
Git push
    ↓
GitHub
    ↓
GitHub Actions
    ↓
Flake8 + Pytest + Coverage
    ↓
Docker build
    ↓
Docker Hub
    ↓
Render Deploy Hook
    ↓
Render
    ↓
Docker container
    ↓
Gunicorn
    ↓
Django
    ↓
Public HTTPS
```

### Render configuration

The service uses the image:

```text
docker.io/tommouquet/orange-county-lettings:latest
```

Production environment variables:

```env
SECRET_KEY=<production-key>
DEBUG=False
ALLOWED_HOSTS=orange-county-lettings-a4ee.onrender.com
SENTRY_DSN=<Sentry-DSN>
SENTRY_ENVIRONMENT=production
```

Do not include:

- `https://` in `ALLOWED_HOSTS`;
- a trailing slash in `ALLOWED_HOSTS`;
- secrets directly in the repository.

Render also provides the listening port used by the container. The Dockerfile includes a fallback to `8000` for local use.

### Public application

https://orange-county-lettings-a4ee.onrender.com/

### Static files

Static files are prepared with:

```bash
python manage.py collectstatic --noinput
```

They are served in production using **WhiteNoise**.

### Production server

Django is not started with `runserver` in production.

The container starts **Gunicorn** with two workers and listens on:

```text
0.0.0.0:${PORT:-8000}
```

### Automatic deployment

After a push to `master`:

1. GitHub Actions runs tests and quality checks;
2. if the checks succeed, the Docker image is built;
3. the image is published to Docker Hub;
4. the Render Deploy Hook is triggered;
5. Render pulls the new image;
6. the service restarts with the new version.

A code change followed by a commit and push to `master` is therefore deployed automatically if the CI pipeline is successful.

---

## Technical Documentation

The project documentation is generated with **Sphinx** and published on **Read the Docs**.

Public documentation:

https://orange-county-lettings-read-the-docs.readthedocs.io/en/latest/

It covers:

- installation;
- architecture;
- database and models;
- usage;
- deployment;
- code reference.

### Structure

Documentation sources are stored in:

```text
docs/
```

The main pages are written in **reStructuredText (`.rst`)**.

`docs/conf.py` contains the Sphinx configuration.

`docs/index.rst` is the main documentation entry point and defines the main navigation through the `toctree`.

The **Autodoc** extension generates part of the code reference from Python docstrings.

### Build the documentation locally

Install documentation dependencies if needed:

```bash
pip install -r docs/requirements.txt
```

Then:

```bash
cd docs
make html
```

The generated HTML is written to:

```text
docs/_build/html/
```

On macOS:

```bash
open _build/html/index.html
```

### Read the Docs

The following file:

```text
.readthedocs.yaml
```

configures the documentation build on Read the Docs.

Read the Docs:

1. clones the GitHub repository;
2. prepares the Python environment;
3. installs the required dependencies;
4. runs Sphinx;
5. publishes the generated documentation on its own domain.

The Read the Docs URL is therefore independent from the Django application URLs.

---

## Useful Commands

### Check Git status

```bash
git status
```

### Run the development server

```bash
python manage.py runserver
```

### Check Django configuration

```bash
python manage.py check
```

### Migrations

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations
python manage.py makemigrations --check --dry-run
```

### Tests

```bash
pytest
```

### Coverage

```bash
pytest --cov=. --cov-report=term-missing --cov-fail-under=80
```

### Flake8

```bash
flake8 oc_lettings_site lettings profiles manage.py
```

### Static files

```bash
python manage.py collectstatic --noinput
```

### Docker build

```bash
docker build -t orange-county-lettings:local .
```

### Docker run

```bash
docker run --rm -p 8000:8000 --env-file .env orange-county-lettings:local
```

### Docker Hub pull

```bash
docker pull tommouquet/orange-county-lettings:latest
```

### Docker Hub run

```bash
docker run --rm \
  -p 8000:8000 \
  --env-file .env \
  tommouquet/orange-county-lettings:latest
```

### Sphinx documentation

```bash
cd docs
make html
```

---

## Security

- Secrets are not stored in the repository.
- `.env` is used only for local configuration.
- `.env` is ignored by Git.
- `.env.example` documents the required variables without containing real secrets.
- CI/CD secrets are stored in GitHub Actions.
- Production environment variables are configured in Render.
- `DEBUG` is disabled in production.
- Sentry is configured through environment variables.
- Docker publication and Render deployment occur only after automated checks succeed.

---

## OpenClassrooms Project

This project was completed as part of the **OpenClassrooms Python Application Developer** path.

The main technical objectives were:

- refactor a monolithic Django application;
- preserve existing data using Django migrations;
- improve code quality;
- add automated tests;
- implement logging and Sentry monitoring;
- create a CI/CD pipeline;
- containerize the application with Docker;
- publish the image on Docker Hub;
- deploy the application to production;
- provide complete technical documentation.
