""" Tests for the root URL configuration. """

from django.urls import resolve, reverse

from oc_lettings_site import views


def test_home_url():
    """ Test that the home URL resolves correctly. """
    url = reverse('index')

    assert resolve(url).func == views.index
