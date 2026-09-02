""" Tests for lettings views. """

import pytest
from unittest.mock import patch

from django.urls import reverse


def test_lettings_index_view(client, letting):
    """ Test the letting index page. """
    response = client.get(reverse('lettings:index'))

    content = response.content.decode()

    assert response.status_code == 200
    assert 'lettings/index.html' in [
        template.name for template in response.templates
    ]
    assert letting in response.context['lettings_list']
    assert letting.title in content


@pytest.mark.django_db
def test_letting_detail_view(client, letting):
    """ Test the letting detail page. """
    response = client.get(
        reverse(
            'lettings:letting',
            args=[letting.id]
        )
    )

    content = response.content.decode()

    assert response.status_code == 200
    assert 'lettings/letting.html' in [
        template.name for template in response.templates
    ]
    assert response.context['title'] == letting.title
    assert response.context['address'] == letting.address
    assert letting.title in content
    assert str(letting.address) in content


@pytest.mark.django_db
def test_missing_letting_returns_404(client):
    """ Test that a missing letting returns HTTP 404 and logs a warning. """
    with patch('lettings.views.logger.warning') as mock_warning:
        response = client.get(
            reverse(
                'lettings:letting',
                args=[999999]
            )
        )

    assert response.status_code == 404

    mock_warning.assert_called_once_with(
        'Letting not found: id=%s.',
        999999,
    )
