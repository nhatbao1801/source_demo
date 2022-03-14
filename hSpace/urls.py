import django_js_reverse.views
from django.conf.urls import url
# from main.admin import admin_site
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.documentation import include_docs_urls
from rest_framework.permissions import IsAdminUser
from django.contrib.admin import AdminSite

from event.models.event import Event

# Tùy biến trang admin
class HinnoxAdminSite(AdminSite):
    site_header = ('Admin site for hSpaces.net')
    site_title = ('Hello from hSpaces.net')
    index_title = ('hSpaces.net')

admin_site = HinnoxAdminSite(name='hSpaces.net admin')

admin_site.register(Event)

schema_view = get_schema_view(
    openapi.Info(
        title="hSpace.biz API",
        default_version='v2',
        description="API for hspace network",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="admin@hspace.biz"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.IsAuthenticated, permissions.IsAdminUser),
)

urlpatterns = [
    path('admin/', admin_site.urls),
    path(
        'admin/password_reset/',
        auth_views.PasswordResetView.as_view(),
        name='admin_password_reset',
    ),
    path(
        'admin/password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete',
    ),
    path('event/', include('event.urls')),
    path('docs/', include_docs_urls(title='hSpaces.net API', description='Sumary API used in the hspaces.net project',
                                    permission_classes=[IsAdminUser]
                                    )),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


# Register models
# admin_site.register(Event)