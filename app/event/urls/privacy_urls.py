from rest_framework.routers import DefaultRouter

from event.views.crud_privacy_viewsets import PrivacyCRUDViewSet

urlpatterns = [

]

# Privacy Router CRUD
privacy_router = DefaultRouter()
privacy_router.register(r'privacy/', PrivacyCRUDViewSet, basename='privacy')
urlpatterns += privacy_router.urls