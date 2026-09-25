Base de données et modèles
==========================

Vue d'ensemble
--------------

Orange County Lettings utilise SQLite comme base de données.

Le fichier de base de données du projet est :

.. code-block:: text

   oc-lettings-site.sqlite3

Django utilise son ORM pour manipuler les données à partir de classes Python.
Chaque modèle Django représente une structure de données stockée en base.

Le projet contient principalement trois modèles :

- ``Address`` : représente une adresse ;
- ``Letting`` : représente une location ;
- ``Profile`` : représente le profil d'un utilisateur.

Modèle ``Address``
------------------

Le modèle ``Address`` est défini dans l'application ``lettings``.

Il contient les informations nécessaires pour représenter une adresse
immobilière :

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

Les validateurs permettent de limiter certaines valeurs.

Par exemple :

- ``number`` ne peut pas dépasser 9999 ;
- ``zip_code`` ne peut pas dépasser 99999 ;
- ``state`` doit contenir au minimum deux caractères ;
- ``country_iso_code`` doit contenir au minimum trois caractères.

Modèle ``Letting``
------------------

Le modèle ``Letting`` est également défini dans l'application ``lettings``.

.. code-block:: python

   class Letting(models.Model):
       title = models.CharField(max_length=256)
       address = models.OneToOneField(
           Address,
           on_delete=models.CASCADE
       )

Une location possède :

- un titre ;
- une adresse.

La relation entre ``Letting`` et ``Address`` est une relation ``OneToOneField``.

Cela signifie qu'une location possède une seule adresse et qu'une adresse
associée à une location ne peut être liée qu'à cette location.

La propriété :

.. code-block:: python

   on_delete=models.CASCADE

indique que si l'adresse associée est supprimée, la location correspondante
est également supprimée.

Modèle ``Profile``
------------------

Le modèle ``Profile`` est défini dans l'application ``profiles``.

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

Chaque profil est associé à un utilisateur Django.

La relation ``OneToOneField`` garantit qu'un utilisateur possède au maximum
un profil associé.

Le champ ``favorite_city`` est optionnel grâce à :

.. code-block:: python

   blank=True

Relations entre les modèles
----------------------------

La structure simplifiée de la base peut être représentée ainsi :

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

Les modèles ``Address`` et ``Letting`` appartiennent à l'application
``lettings``.

Le modèle ``Profile`` appartient à l'application ``profiles`` et utilise le
modèle ``User`` fourni par Django.

ORM Django
----------

L'ORM de Django permet d'interagir avec la base de données en Python sans
écrire directement de requêtes SQL.

Par exemple, la récupération d'une location peut être réalisée avec une
instruction Python telle que :

.. code-block:: python

   Letting.objects.get(id=letting_id)

Django traduit ensuite automatiquement cette instruction en requête SQL
adaptée à la base de données.

Migrations
----------

Les migrations permettent de faire évoluer la structure de la base de données
de manière versionnée.

Deux commandes principales sont utilisées :

.. code-block:: bash

   python manage.py makemigrations
   python manage.py migrate

``makemigrations`` génère les fichiers décrivant les changements apportés aux
modèles.

``migrate`` applique ces migrations à la base de données.

Lors de la refactorisation du projet, les modèles ont été déplacés vers les
applications ``lettings`` et ``profiles`` tout en conservant les données
existantes grâce au système de migrations Django.

Cette approche permet d'éviter la manipulation directe de la base avec des
requêtes SQL manuelles.