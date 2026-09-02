""" Tests for profiles URLs. """

from django.urls import resolve, reverse

from profiles import views


def test_profiles_index_url():
    """ Test that the profiles index URL resolves correctly. """
    url = reverse('profiles:index')

    assert resolve(url).func == views.index


def test_profile_detail_url():
    """ Test that a profile detail URL resolves correctly. """
    url = reverse('profiles:profile', args=['john'])

    assert resolve(url).func == views.profile
