""" Views for the profiles application. """

import logging

from django.http import Http404
from django.shortcuts import render

from .models import Profile


logger = logging.getLogger(__name__)


def index(request):
    """ Display all user profiles. """
    logger.info('Displaying profiles list.')

    profiles_list = Profile.objects.all()

    context = {'profiles_list': profiles_list}

    return render(request, 'profiles/index.html', context)


def profile(request, username):
    """ Display the profile associated with a username. """
    try:
        profile = Profile.objects.get(user__username=username)
    except Profile.DoesNotExist:
        logger.warning(
            'Profile not found: username=%s.',
            username,
        )
        raise Http404('Profile not found.')

    logger.info(
        'Displaying profile with username=%s.',
        username,
    )

    context = {'profile': profile}

    return render(request, 'profiles/profile.html', context)
