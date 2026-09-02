""" Views for the lettings application. """

import logging

from django.http import Http404
from django.shortcuts import render

from .models import Letting


logger = logging.getLogger(__name__)


def index(request):
    """ Display all available lettings. """
    logger.info('Displaying lettings list.')

    lettings_list = Letting.objects.all()

    context = {'lettings_list': lettings_list}

    return render(request, 'lettings/index.html', context)


def letting(request, letting_id):
    """ Display the details of a letting identified by its ID. """
    try:
        letting = Letting.objects.get(id=letting_id)
    except Letting.DoesNotExist:
        logger.warning(
            'Letting not found: id=%s.',
            letting_id,
        )
        raise Http404('Letting not found.')

    logger.info(
        'Displaying letting: id=%s.',
        letting_id,
    )

    context = {
        'title': letting.title,
        'address': letting.address,
    }

    return render(request, 'lettings/letting.html', context)
