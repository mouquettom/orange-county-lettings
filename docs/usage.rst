Utilisation de l'application
============================

Présentation
------------

Orange County Lettings est une application de consultation de locations
immobilières et de profils utilisateurs.

L'application est principalement destinée à la consultation des données.
Les différentes pages permettent de naviguer entre les locations, leurs
adresses et les profils enregistrés.

Page d'accueil
--------------

La page d'accueil est accessible à la racine du site :

.. code-block:: text

   /

Elle permet d'accéder aux deux fonctionnalités principales :

- les locations ;
- les profils utilisateurs.

Consultation des locations
---------------------------

La page des locations permet d'afficher la liste des biens disponibles.

Elle est accessible depuis la navigation principale du site.

Pour chaque location, l'utilisateur peut consulter une page de détail contenant
notamment :

- le titre de la location ;
- le numéro et la rue ;
- la ville ;
- l'État ;
- le code postal ;
- le code pays.

Le fonctionnement peut être résumé ainsi :

.. code-block:: text

   Page d'accueil
        |
        v
   Liste des locations
        |
        v
   Détail d'une location
        |
        v
   Adresse associée

Consultation des profils
-------------------------

La page des profils permet d'afficher les utilisateurs disposant d'un profil
dans l'application.

L'utilisateur peut ensuite sélectionner un profil afin d'accéder à sa page
de détail.

Cette page affiche notamment :

- le nom d'utilisateur ;
- la ville favorite du profil lorsqu'elle est renseignée.

Le parcours correspondant est :

.. code-block:: text

   Page d'accueil
        |
        v
   Liste des profils
        |
        v
   Détail d'un profil

Administration Django
---------------------

L'application dispose également de l'interface d'administration intégrée à
Django.

Elle est accessible à l'adresse :

.. code-block:: text

   /admin/

Cette interface est réservée aux utilisateurs disposant des droits
d'administration nécessaires.

Elle permet notamment de consulter et gérer les données enregistrées dans la
base.

Pages d'erreur
--------------

Des pages personnalisées sont prévues pour les principales erreurs HTTP.

Erreur 404
~~~~~~~~~~

Une erreur HTTP 404 est retournée lorsqu'un utilisateur demande une ressource
ou une URL qui n'existe pas.

L'application affiche alors une page personnalisée plutôt que la page d'erreur
technique par défaut de Django.

Erreur 500
~~~~~~~~~~

Une erreur HTTP 500 correspond à une erreur interne survenue pendant le
traitement d'une requête.

En production, lorsque ``DEBUG=False``, l'utilisateur voit une page d'erreur
personnalisée sans obtenir les informations techniques internes de
l'application.

Cas d'utilisation principaux
-----------------------------

Les principaux cas d'utilisation sont les suivants :

1. consulter la page d'accueil ;
2. consulter la liste des locations ;
3. afficher le détail d'une location et son adresse ;
4. consulter la liste des profils ;
5. afficher le détail d'un profil ;
6. administrer les données via l'interface Django pour un utilisateur autorisé.

Navigation
----------

La navigation générale peut être représentée ainsi :

.. code-block:: text

                        Accueil
                       /       \
                      /         \
                     v           v
              Locations       Profils
                  |               |
                  v               v
          Détail location   Détail profil


                  Administration
                       |
                       v
                    /admin/