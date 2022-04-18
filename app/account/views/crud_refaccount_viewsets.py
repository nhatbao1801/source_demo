import logging
from rest_framework import status
from django.http import JsonResponse

from account.models.account import RefAccount
from account.schemas.media_schema import AccountSchemas
from account.serializers.ref_account_serializer import (
    RefAccountSerializerIn, RefAccountSerializerOut)
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, pagination, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from utils.base_class_schema_pagination import PaginatorInspectorClass
from utils.paginator import s_paginator

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s:%(levelname)s:%(module)s:%(lineno)d:%(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
class RefAccountViewSet(mixins.ListModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet, mixins.CreateModelMixin):
    """ViewSet for Ref Account"""
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [AllowAny]
    serializer_class = RefAccountSerializerIn
    queryset = RefAccount.objects.all()
    pagination_class = pagination.PageNumberPagination

    def get_serializer_class(self):
        if 'list' in self.action:
            self.serializer_class = RefAccountSerializerOut
        return super().get_serializer_class()

    @swagger_auto_schema(paginator_inspectors=[PaginatorInspectorClass])
    def list(self, request, *args, **kwargs):
        _serializer = self.get_serializer_class()
        data, metadata = s_paginator(object_list=self.get_queryset(), request=request)
        data_serializer = _serializer(data, many=True, context={'request': request}).data
        return JsonResponse(
            data={
                'data': data_serializer,
                'metadata': metadata
            }, status=status.HTTP_200_OK
        )

    @swagger_auto_schema(request_body=RefAccountSerializerIn)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
