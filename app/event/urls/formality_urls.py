from rest_framework.routers import DefaultRouter

from event.views.crud_formality_viewsets import FormalityCRUDViewSet

urlpatterns = [

]

# Formality Router CRUD
formalityt_router = DefaultRouter()
formalityt_router.register(r'formality', FormalityCRUDViewSet, basename='formality')
urlpatterns += formalityt_router.urls