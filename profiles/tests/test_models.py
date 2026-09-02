""" Tests for profiles models """

import pytest
from django.contrib.auth.models import User

from profiles.models import Profile


@pytest.mark.django_db
def test_profile_string_representation():
    """ Test the string representation of a profile. """
    user = User.objects.create(
        username='john',
        password='password123',
    )

    profile = Profile.objects.create(
        user=user,
        favorite_city='Los Angeles',
    )

    assert str(profile) == 'john'
