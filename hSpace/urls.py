from typing import Type
import django_js_reverse.views
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.documentation import include_docs_urls
from rest_framework.permissions import IsAdminUser
from django.contrib.admin import AdminSite
from event.models.area import Area
from event.models.city import City
from event.models.organization import Organization
from event.models.team import Team
from event.models.type import Type as type_model
from event.models.event import Event
from event.models.event_category import EventCategory
from event.models.event_participant import EventParticipant
from event.models.event_type import EventType
from event.models.sponsor_event import SponsorEvent
from event.models.media import Media
from event.models.ticket import Ticket
from event.views.set_get_data_views import EventViewSet


# Tùy biến trang admin
class HinnoxAdminSite(AdminSite):
    site_header = ('Admin site for hSpaces.net')
    site_title = ('Hello from hSpaces.net')
    index_title = ('hSpaces.net')

admin_site = HinnoxAdminSite(name='hSpaces.net admin')

admin_site.register(Event) # addevent
admin_site.register(EventParticipant)  # Danh sách người tham gia event
admin_site.register(EventCategory)  # Danh sách nhà tài trợ
admin_site.register(EventType)  # loại event
admin_site.register(SponsorEvent)  #Danh sách các nhà tài trợ cho các sự kiện
admin_site.register(Media)  # medias của event
admin_site.register(Ticket)  # thông tin ticket của event
admin_site.register(Area)
admin_site.register(City)
admin_site.register(Team)
admin_site.register(Organization)


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
    # permission_classes=(permissions.IsAuthenticated, permissions.IsAdminUser),
)

urlpatterns = [
    path('', admin_site.urls),
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
    path('docs/', include_docs_urls(title='hSpaces.net API', description='Sumary API used in the hspaces.net project')),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


# Register models
# admin_site.register(Event)