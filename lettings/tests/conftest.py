""" Fixture for lettings tests. """

import pytest

from lettings.models import Address, Letting


@pytest.fixture
def address(db):
    """ Create an address for tests. """
    return Address.objects.create(
        number=12,
        street='Main Street',
        city='Los Angeles',
        state='CA',
        zip_code=90001,
        country_iso_code='USA',
    )


@pytest.fixture
def letting(address):
    """ Create a letting associated with an address. """
    return Letting.objects.create(
        title='Stunning apartment in the hills of Los Angeles',
        address=address,
    )
