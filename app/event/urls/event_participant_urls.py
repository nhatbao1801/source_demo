from rest_framework.routers import DefaultRouter
from django.urls import path
from event.views.crud_event_participant_viewsets import EventParticipantCRUDViewSet

urlpatterns = [
]

# Event participant Router CRUD
event_participant_router = DefaultRouter()
event_participant_router.register(r'event-participant', EventParticipantCRUDViewSet, basename='event')
urlpatterns += event_participant_router.urls