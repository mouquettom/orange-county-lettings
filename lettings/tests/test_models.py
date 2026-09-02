""" Tests for lettings models. """

import pytest

from lettings.models import Address, Letting


@pytest.mark.django_db
def test_address_string_representation(address):
    """ Test the string representation of an address. """
    assert str(address) == '12 Main Street'


@pytest.mark.django_db
def test_letting_string_representation(letting):
    """ Test the string representation of a letting. """
    assert str(letting) == 'Stunning apartment in the hills of Los Angeles'


def test_address_plural_name():
    """ Test the custom plural name of Address. """
    assert Address._meta.verbose_name_plural == 'Addresses'
