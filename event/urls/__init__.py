from django.urls import path

from event.urls import ajax, api

app_name = 'event'

urlpatterns = ajax.urlpatterns
urlpatterns += api.urlpatterns
