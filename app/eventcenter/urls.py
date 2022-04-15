import logging
from urllib.parse import urlsplit

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, reverse, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.request import Request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(module)s:%(lineno)d:%(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


def get_current_host(self, request: Request) -> str:
    # TODO: Stup https for scheme
    scheme = request.scheme
    logger.info(f'{scheme}---{request.get_host()}')
    return f'https://{request.get_host()}'


def home(request):
    host_scheme = "{}".format(get_current_host(self=request, request=request))
    doc_link = "{}{}".format(host_scheme, reverse('schema-doc'))
    swagger_link = "{}{}".format(host_scheme, reverse('schema-swagger-ui'))
    admin_link = "{}{}".format(host_scheme, '/admin/')
    ref_links = [
        {
            "docs": doc_link,
        }, {
            "swagger": swagger_link,
        }, {
            "admin": admin_link,
        }
    ]
    return JsonResponse({"welcome": "Welcome to eventcenter.api.hspace.biz \n CI Deploy", "ref_links": ref_links})


urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
]

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

schema_view = get_schema_view(
    openapi.Info(
        title="eventcenter.api.hspace.biz",
        default_version='v1',
        description="eventcenter API Docs",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@hspace.biz"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    # permission_classes=(permissions.IsAuthenticated, permissions.IsAdminUser),
    permission_classes=(permissions.AllowAny,),
)

# Docs urls
urlpatterns += [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-doc'),
]

# All apps urls
urlpatterns += [
    path('account/', include('account.urls')),
    path('event/', include('event.urls')),
]
