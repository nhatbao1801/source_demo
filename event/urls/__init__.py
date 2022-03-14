from django.urls import path

from event.urls import api

app_name = 'event'

urlpatterns = api.urlpatterns
