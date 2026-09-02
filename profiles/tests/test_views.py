""" Test profiles views. """

import pytest
from unittest.mock import patch

from django.contrib.auth.models import User
from django.urls import reverse

from profiles.models import Profile


@pytest.mark.django_db
def test_profiles_index_view(client):
    """ Test the profile index page. """
    response = client.get(reverse('profiles:index'))

    assert response.status_code == 200
    assert 'profiles/index.html' in [
        template.name for template in response.templates
    ]


@pytest.mark.django_db
def test_profile_detail_view(client):
    """ Test the profile detail page. """
    user = User.objects.create_user(
        username='john',
        password='password123',
        first_name='John',
        last_name='Doe',
    )

    profile = Profile.objects.create(
        user=user,
        favorite_city='Los Angeles',
    )

    response = client.get(
        reverse('profiles:profile', args=[user.username])
    )

    assert response.status_code == 200
    assert response.context['profile'] == profile


@pytest.mark.django_db
def test_missing_profile_returns_404(client):
    """ Test that a missing profile returns HTTP 404 and logs a warning. """
    with patch('profiles.views.logger.warning') as mock_warning:
        response = client.get(
            reverse('profiles:profile', args=['unknown-user'])
        )

    assert response.status_code == 404

    mock_warning.assert_called_once_with(
        'Profile not found: username=%s.',
        'unknown-user',
    )
