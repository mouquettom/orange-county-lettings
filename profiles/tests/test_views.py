""" Test profiles views. """

from unittest.mock import patch
import pytest

from django.urls import reverse


def test_profiles_index_view(client, profile):
    """ Test the profile index page. """
    response = client.get(reverse('profiles:index'))

    content = response.content.decode()

    assert response.status_code == 200
    assert 'profiles/index.html' in [
        template.name for template in response.templates
    ]
    assert profile in response.context['profiles_list']
    assert profile.user.username in content


def test_profile_detail_view(client, profile):
    """ Test the profile detail page. """
    response = client.get(
        reverse(
            'profiles:profile',
            args=[profile.user.username]
        )
    )

    content = response.content.decode()

    assert response.status_code == 200
    assert 'profiles/profile.html' in [
        template.name for template in response.templates
    ]
    assert response.context['profile'] == profile
    assert profile.user.username in content
    assert profile.user.first_name in content
    assert profile.user.last_name in content
    assert profile.favorite_city in content


@pytest.mark.django_db
def test_missing_profile_returns_404(client):
    """ Test that a missing profile returns HTTP 404 and logs a warning. """
    with patch('profiles.views.logger.warning') as mock_warning:
        response = client.get(
            reverse(
                'profiles:profile',
                args=['unknown-user']
            )
        )

    assert response.status_code == 404

    mock_warning.assert_called_once_with(
        'Profile not found: username=%s.',
        'unknown-user',
    )
