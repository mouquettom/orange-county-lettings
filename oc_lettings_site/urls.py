""" Root URL configuration for Orange County Lettings. """

from django.contrib import admin
from django.urls import include, path

from . import views


handler404 = views.custom_404
handler500 = views.custom_500


urlpatterns = [
    path('', views.index, name='index'),
    path('sentry-debug/', views.trigger_sentry_error, name='sentry-debug'),
    path('lettings/', include('lettings.urls')),
    path('profiles/', include('profiles.urls')),
    path('admin/', admin.site.urls),
]
