""" Fixture for profiles tests. """

import pytest
from django.contrib.auth.models import User

from profiles.models import Profile


@pytest.fixture
def profile(db):
    """ Create a profile and its associated user for tests. """
    user = User.objects.create_user(
        username='john',
        password='password123',
        first_name='John',
        last_name='Doe',
        email='john@example.com',
    )

    return Profile.objects.create(
        user=user,
        favorite_city='Los Angeles',
    )
