from rest_framework.routers import DefaultRouter

from event.views.crud_event_type_viewsets import EventTypeCRUDViewSet

urlpatterns = [

]

# Event Type Router CRUD
event_type_router = DefaultRouter()
event_type_router.register(r'event-type', EventTypeCRUDViewSet, basename='event-type')
urlpatterns += event_type_router.urls