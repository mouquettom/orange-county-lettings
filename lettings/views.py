""" Views for the lettings application. """

from django.shortcuts import render

from .models import Letting


def index(request):
    """ Display all available lettings. """
    lettings_list = Letting.objects.all()

    context = {'lettings_list': lettings_list}

    return render(
        request,
        'lettings/index.html',
        context
    )


def letting(request, letting_id):
    """ Display the details of a letting identified by its ID. """
    letting = Letting.objects.get(id=letting_id)

    context = {
        'title': letting.title,
        'address': letting.address,
    }

    return render(
        request,
        'lettings/letting.html',
        context
    )
