import logging
from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, pagination, status, viewsets
from rest_framework.permissions import AllowAny
from event.models.event_type import EventType
from event.serializers.event_type_serializer import EventTypeSerializer, EventTypeSerializerOut
from utils.base_class_schema_pagination import PaginatorInspectorClass
from utils.paginator import s_paginator

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s:%(levelname)s:%(module)s:%(lineno)d:%(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


class EventTypeCRUDViewSet(
        mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, 
        mixins.UpdateModelMixin, mixins.DestroyModelMixin,viewsets.GenericViewSet
    ):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = EventTypeSerializer
    queryset = EventType.objects.all()
    pagination_class = pagination.PageNumberPagination

    def get_serializer_class(self):
        if 'list' in self.action or 'retrieve' in self.action:
            self.serializer_class = EventTypeSerializerOut
        return super().get_serializer_class()

    @swagger_auto_schema(
        operation_summary='Danh sách loại loại sự kiện',
        manual_parameters=[
            openapi.Parameter(
                'page', type=openapi.TYPE_INTEGER, in_=openapi.IN_QUERY,
                description='Số trang'
            ),
            openapi.Parameter(
                'limit', type=openapi.TYPE_INTEGER, in_=openapi.IN_QUERY,
                description='Số items trên một trang'
            ),
        ], paginator_inspectors=[PaginatorInspectorClass], tags=['event-type']
    )
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

    @swagger_auto_schema(
        operation_summary='Tạo mới loại sự kiện', tags=['event-type']
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Chi tiết loại sự kiện', tags=['event-type']
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    
    @swagger_auto_schema(
        operation_summary='Cập nhật loại sự kiện', tags=['event-type']
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Cập nhật loại sự kiện', tags=['event-type'],
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


    @swagger_auto_schema(
        operation_summary='Xóa loại sự kiện', tags=['event-type']
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
