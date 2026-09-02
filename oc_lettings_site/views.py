""" Main views and error handlers for Orange County Lettings. """

from django.shortcuts import render


def index(request):
    """ Display the application's home page. """
    return render(request, 'index.html')


def custom_404(request, exception):
    """ Render the custom page for HTTP 404 errors. """
    return render(request, '404.html', status=404)


def custom_500(request):
    """ Render the custom page for HTTP 500 errors. """
    return render(request, '500.html', status=500)
