Using the Application
=====================

Presentation
------------

Orange County Lettings is an application for browsing property lettings and
user profiles.

The application is mainly intended for viewing data. Its pages let users
navigate between lettings, their addresses and registered profiles.

Home page
---------

The home page is available at the root of the site:

.. code-block:: text

   /

It gives access to the two main features:

- lettings;
- user profiles.

Browsing lettings
-----------------

The lettings page displays the list of available properties.

It is reachable from the site's main navigation.

For each letting, the user can open a detail page showing, among other things:

- the title of the letting;
- the street number and name;
- the city;
- the state;
- the ZIP code;
- the country code.

The flow can be summarized as follows:

.. code-block:: text

   Home page
        |
        v
   Lettings list
        |
        v
   Letting details
        |
        v
   Associated address

Browsing profiles
-----------------

The profiles page displays the users who have a profile in the application.

The user can then select a profile to open its detail page.

This page shows, among other things:

- the username;
- the profile's favorite city, when provided.

The corresponding flow is:

.. code-block:: text

   Home page
        |
        v
   Profiles list
        |
        v
   Profile details

Django administration
---------------------

The application also provides Django's built-in administration interface.

It is available at:

.. code-block:: text

   /admin/

This interface is restricted to users with the required administration
rights.

It can be used to view and manage the data stored in the database.

Error pages
-----------

Custom pages are provided for the main HTTP errors.

404 error
~~~~~~~~~

An HTTP 404 error is returned when a user requests a resource or URL that does
not exist.

The application then displays a custom page instead of Django's default
technical error page.

500 error
~~~~~~~~~

An HTTP 500 error corresponds to an internal error raised while processing a
request.

In production, when ``DEBUG=False``, the user sees a custom error page without
any internal technical details about the application.

Main use cases
--------------

The main use cases are:

1. view the home page;
2. view the list of lettings;
3. display the details of a letting and its address;
4. view the list of profiles;
5. display the details of a profile;
6. manage the data through the Django interface as an authorized user.

Navigation
----------

The overall navigation can be represented as follows:

.. code-block:: text

                         Home
                       /       \
                      /         \
                     v           v
               Lettings       Profiles
                  |               |
                  v               v
          Letting details   Profile details


                  Administration
                       |
                       v
                    /admin/