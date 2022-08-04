import logging

from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from account.serializers.ref_account_serializer import EventParcitipantSerializerInfo
from account.models.account import RefAccount
from utils.get_provider_alive.get_provider_alive import get_profile_detail
from event.serializers.event_participant_serializer import EventParticipantOut, EventParticipantSerializer
from event.models.event_participant import EventParticipant
from event.models.event import Event
from event.serializers.event_serializer import (EventSerializer,
                                                EventSerializerOut)
from rest_framework import mixins, pagination, status, viewsets
from rest_framework.permissions import AllowAny
from utils.base_class_schema_pagination import PaginatorInspectorClass
from utils.paginator import s_paginator
from rest_framework.views import APIView
from rest_framework.response import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s:%(levelname)s:%(module)s:%(lineno)d:%(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


class EventParticipantCRUDViewSet(
        mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, 
        mixins.UpdateModelMixin, mixins.DestroyModelMixin,viewsets.GenericViewSet
    ):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = EventParticipantSerializer
    queryset = EventParticipant.objects.filter(is_deleted=False)
    pagination_class = pagination.PageNumberPagination

    def get_serializer_class(self):
        if 'list' in self.action or 'retrieve' in self.action:
            self.serializer_class = EventParticipantOut
        return super().get_serializer_class()

    @swagger_auto_schema(
        operation_summary='Danh sách participant',
        manual_parameters=[
            openapi.Parameter(
                'page', type=openapi.TYPE_INTEGER, in_=openapi.IN_QUERY,
                description='Số trang'
            ),
            openapi.Parameter(
                'limit', type=openapi.TYPE_INTEGER, in_=openapi.IN_QUERY,
                description='Số items trên một trang'
            ),
            openapi.Parameter(
                'event_id', type=openapi.TYPE_INTEGER, in_=openapi.IN_QUERY,
                description='Số items trên một trang', default=None
            ),
        ], paginator_inspectors=[PaginatorInspectorClass], tags=['event-participant']
    )
    def list(self, request, *args, **kwargs):
        _queryset = list(EventParticipant.objects.filter(is_deleted=False, event_id=request.GET.get('event_id')).values_list('uid', flat=True))
        data, metadata = s_paginator(object_list=_queryset, request=request, not_queryset=True)
        data_serializer = []
        for i in data:
            profile = get_profile_detail(uid=i)
            data_serializer.append(profile)
        # data_serializer = _serializer(data, many=True, context={'request': request}).data
        return JsonResponse(
            data={
                'data': data_serializer,
                'metadata': metadata
            }, status=status.HTTP_200_OK
        )


    @swagger_auto_schema(
        operation_summary='Xóa participant', tags=['event-participant']
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return JsonResponse(
            data={
                'status': 'HTTP_200_OK',
                'msg': 'Removed'
            }, status=status.HTTP_200_OK
        )