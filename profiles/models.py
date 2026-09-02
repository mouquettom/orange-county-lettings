""" Database models for the profiles application. """

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """ Represent additionnal information associated with a user. """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_city = models.CharField(max_length=64, blank=True)

    def __str__(self):
        """ Return the username associated with the profile. """
        return self.user.username
