""" Tests for the main project views. """

from django.test import RequestFactory, override_settings
from django.urls import reverse

from oc_lettings_site import views


def test_home_page(client):
    """ Test the home page. """
    response = client.get(reverse('index'))

    content = response.content.decode()

    assert response.status_code == 200
    assert 'index.html' in [
        template.name for template in response.templates
    ]
    assert 'Welcome to Holiday Homes' in content


@override_settings(
    DEBUG=False,
    ALLOWED_HOSTS=['testserver'],
)
def test_custom_404_page(client):
    """ Test the custom HTTP 404 page. """
    response = client.get('/page-that-does-not-exist/')

    content = response.content.decode()

    assert response.status_code == 404
    assert '404.html' in [
        template.name for template in response.templates
    ]
    assert 'Page not found' in content


def test_custom_500_pages():
    """ The test custom HTTP 500 handler. """
    request = RequestFactory().get('/')

    response = views.custom_500(request)

    content = response.content.decode()

    assert response.status_code == 500
    assert 'Server error' in content
