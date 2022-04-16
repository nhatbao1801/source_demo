from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from event.urls import event_urls, event_type_urls, formality_urls, privacy_urls

app_name = 'event'

urlpatterns = [
]
urlpatterns += event_urls.urlpatterns
urlpatterns += event_type_urls.urlpatterns
urlpatterns += formality_urls.urlpatterns
urlpatterns += privacy_urls.urlpatterns
