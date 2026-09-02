""" Tests for lettings views. """

import pytest
from unittest.mock import patch

from django.urls import reverse

from lettings.models import Address, Letting


@pytest.mark.django_db
def test_lettings_index_view(client):
    """ Test the letting index page. """
    response = client.get(reverse('lettings:index'))

    assert response.status_code == 200
    assert 'lettings/index.html' in [
        template.name for template in response.templates
    ]


@pytest.mark.django_db
def test_letting_detail_view(client):
    """ Test the letting detail page. """
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

    response = client.get(
        reverse('lettings:letting', args=[letting.id])
    )

    assert response.status_code == 200
    assert response.context['title'] == 'Stunning apartment in the hills of Los Angeles'
    assert response.context['address'] == address


@pytest.mark.django_db
def test_missing_letting_returns_404(client):
    """ Test that a missing letting returns HTTP 404 and logs a warning. """
    with patch('lettings.views.logger.warning') as mock_warning:
        response = client.get(
            reverse('lettings:letting', args=[999999])
        )

    assert response.status_code == 200

    mock_warning.assert_called_once_with(
        'Letting not found: id=%s.',
        999999,
    )