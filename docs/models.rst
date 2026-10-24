Database and Models
===================

Overview
--------

Orange County Lettings uses SQLite as its database.

The project's database file is:

.. code-block:: text

   oc-lettings-site.sqlite3

Django uses its ORM to handle data through Python classes. Each Django model
represents a data structure stored in the database.

The project mainly contains three models:

- ``Address``: represents an address;
- ``Letting``: represents a letting;
- ``Profile``: represents a user's profile.

``Address`` model
-----------------

The ``Address`` model is defined in the ``lettings`` application.

It contains the information needed to represent a property address:

.. code-block:: python

   class Address(models.Model):
       number = models.PositiveIntegerField(
           validators=[MaxValueValidator(9999)]
       )
       street = models.CharField(max_length=64)
       city = models.CharField(max_length=64)
       state = models.CharField(
           max_length=2,
           validators=[MinLengthValidator(2)]
       )
       zip_code = models.PositiveIntegerField(
           validators=[MaxValueValidator(99999)]
       )
       country_iso_code = models.CharField(
           max_length=3,
           validators=[MinLengthValidator(3)]
       )

The validators restrict some values.

For example:

- ``number`` cannot exceed 9999;
- ``zip_code`` cannot exceed 99999;
- ``state`` must contain at least two characters;
- ``country_iso_code`` must contain at least three characters.

``Letting`` model
-----------------

The ``Letting`` model is also defined in the ``lettings`` application.

.. code-block:: python

   class Letting(models.Model):
       title = models.CharField(max_length=256)
       address = models.OneToOneField(
           Address,
           on_delete=models.CASCADE
       )

A letting has:

- a title;
- an address.

The relationship between ``Letting`` and ``Address`` is a ``OneToOneField``
relationship.

This means that a letting has a single address, and an address associated with
a letting can only be linked to that letting.

The option:

.. code-block:: python

   on_delete=models.CASCADE

means that if the associated address is deleted, the corresponding letting is
deleted as well.

``Profile`` model
-----------------

The ``Profile`` model is defined in the ``profiles`` application.

.. code-block:: python

   class Profile(models.Model):
       user = models.OneToOneField(
           User,
           on_delete=models.CASCADE
       )
       favorite_city = models.CharField(
           max_length=64,
           blank=True
       )

Each profile is associated with a Django user.

The ``OneToOneField`` relationship guarantees that a user has at most one
associated profile.

The ``favorite_city`` field is optional thanks to:

.. code-block:: python

   blank=True

Relationships between models
----------------------------

The simplified database structure can be represented as follows:

.. code-block:: text

   User
     │
     │ 1 - 1
     ▼
   Profile


   Address
     │
     │ 1 - 1
     ▼
   Letting

The ``Address`` and ``Letting`` models belong to the ``lettings`` application.

The ``Profile`` model belongs to the ``profiles`` application and uses the
``User`` model provided by Django.

Django ORM
----------

The Django ORM makes it possible to interact with the database in Python
without writing SQL queries directly.

For example, a letting can be retrieved with a Python statement such as:

.. code-block:: python

   Letting.objects.get(id=letting_id)

Django then automatically translates this statement into an SQL query suited
to the database.

Migrations
----------

Migrations make it possible to evolve the database structure in a versioned
way.

Two main commands are used:

.. code-block:: bash

   python manage.py makemigrations
   python manage.py migrate

``makemigrations`` generates the files describing the changes made to the
models.

``migrate`` applies these migrations to the database.

During the refactoring, the models were moved to the ``lettings`` and
``profiles`` applications while preserving the existing data through the
Django migration system.

This approach avoids manipulating the database directly with manual SQL
queries.
