from rest_framework.routers import DefaultRouter
from django.urls import path
from event.views.crud_event_viewsets import EventCRUDViewSet, InviteEventAPI, JoinEventAPI

urlpatterns = [
    path('join-event/', JoinEventAPI.as_view(), name='join-event'),
    path('invite-event/', InviteEventAPI.as_view(), name='invite-event'),
]

# Event Router CRUD
event_router = DefaultRouter()
event_router.register(r'event', EventCRUDViewSet, basename='event')
urlpatterns += event_router.urls