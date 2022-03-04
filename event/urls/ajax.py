from django.urls import path

from event.views import set_data_views

urlpatterns = [
    path('profile/update-avatar/', set_data_views.event_upload_avatar, name='event-upload-avatar'),
    path('profile/update-cover/', set_data_views.event_upload_cover, name='event-upload-cover'),
]
