from rest_framework.routers import DefaultRouter

from event.views.crud_event_viewsets import EventCRUDViewSet

urlpatterns = [

]

# Event Router CRUD
event_router = DefaultRouter()
event_router.register(r'event', EventCRUDViewSet, basename='event')
urlpatterns += event_router.urls