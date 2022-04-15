from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from account.urls import account_urls

app_name = 'account'

urlpatterns = [
]
# Login urls
urlpatterns += [
    # LOGIN API
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += account_urls.urlpatterns
