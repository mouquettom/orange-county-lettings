""" Tests for profiles models """


def test_profile_string_representation(profile):
    """ Test the string representation of a profile. """
    assert str(profile) == 'john'
