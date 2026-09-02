""" Tests for lettings URLs. """

from django.urls import resolve, reverse

from lettings import views


def test_lettings_index_url():
    """ Test that the lettings index URL resolves correctly. """
    url = reverse('lettings:index')

    assert resolve(url).func == views.index


def test_letting_detail_url():
    """ Test that a letting detail URL resolves correctly. """
    url = reverse('lettings:letting', args=[1])

    assert resolve(url).func == views.letting
