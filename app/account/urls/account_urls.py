from rest_framework.routers import DefaultRouter

from account.views.crud_refaccount_viewsets import RefAccountViewSet

urlpatterns = [

]

# Reference ACCOUNT CRUD
reference_account_router = DefaultRouter()
reference_account_router.register(r'ref_account', RefAccountViewSet, basename='ref_account')
urlpatterns += reference_account_router.urls
