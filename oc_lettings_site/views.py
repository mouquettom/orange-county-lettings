""" Main views and error handlers for Orange County Lettings. """

from django.shortcuts import render


def index(request):
    """ Display the application's home page. """
    return render(request, 'index.html')
