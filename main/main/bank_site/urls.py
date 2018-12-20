from . import views
from django.conf.urls import url
from django.urls import include


urlpatterns = [
    url(r'^accounts/', include('django.contrib.auth.urls')),
]