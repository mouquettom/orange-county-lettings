""" Tests for lettings models. """

import pytest

from lettings.models import Address, Letting


@pytest.mark.django_db
def test_address_string_representation():
    """ Test the string representation of an address. """
    address = Address.objects.create(
        number=12,
        street='Main Street',
        city='Los Angeles',
        state='CA',
        zip_code=90001,
        country_iso_code='USA',
    )

    assert str(address) == '12 Main Street'


@pytest.mark.django_db
def test_letting_string_representation():
    """ Test the string representation of a letting. """
    address = Address.objects.create(
        number=12,
        street='Main Street',
        city='Los Angeles',
        state='CA',
        zip_code=90001,
        country_iso_code='USA',
    )

    letting = Letting.objects.create(
        title='Stunning apartment in the hills of Los Angeles',
        address=address,
    )

    assert str(letting) == 'Stunning apartment in the hills of Los Angeles'


def test_address_plural_name():
    """ Test the custom plural name of Address. """
    assert Address._meta.verbose_name_plural == 'Addresses'
