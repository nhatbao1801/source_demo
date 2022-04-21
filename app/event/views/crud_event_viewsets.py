import logging

from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
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


class EventCRUDViewSet(
        mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, 
        mixins.UpdateModelMixin, mixins.DestroyModelMixin,viewsets.GenericViewSet
    ):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = EventSerializer
    queryset = Event.objects.all().order_by('-from_date')
    pagination_class = pagination.PageNumberPagination

    def get_serializer_class(self):
        if 'list' in self.action or 'retrieve' in self.action:
            self.serializer_class = EventSerializerOut
        return super().get_serializer_class()

    @swagger_auto_schema(
        operation_summary='Danh sách sự kiện',
        manual_parameters=[
            openapi.Parameter(
                'page', type=openapi.TYPE_INTEGER, in_=openapi.IN_QUERY,
                description='Số trang'
            ),
            openapi.Parameter(
                'limit', type=openapi.TYPE_INTEGER, in_=openapi.IN_QUERY,
                description='Số items trên một trang'
            ),
        ], paginator_inspectors=[PaginatorInspectorClass], tags=['event']
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
        operation_summary='Tạo mới sự kiện', tags=['event']
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Chi tiết sự kiện', tags=['event']
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    
    @swagger_auto_schema(
        operation_summary='Cập nhật sự kiện', tags=['event']
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Cập nhật sự kiện', tags=['event'],
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


    @swagger_auto_schema(
        operation_summary='Xóa sự kiện', tags=['event']
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return JsonResponse(
            data={
                'status': 'HTTP_200_OK',
                'msg': 'Success'
            }, status=status.HTTP_200_OK
        )

class JoinEventAPI(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description='Tham gia sự kiện',
        operation_summary='Tham gia sự kiện',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "event_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                "uid": openapi.Schema(type=openapi.TYPE_INTEGER)
            }
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='', examples={
                    "status": "Update successfully"
                }
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description='', examples={
                    "status": "Event not found",
                }
            )
        }
    )
    def post(self, request, *args, **kwargs): 
        try:
            event = Event.objects.get(id=request.data.get('event_id'))
        except Event.DoesNotExist:
            return Response(data={"Missing param event_id"}, status=status.HTTP_400_BAD_REQUEST)

        event_participant = EventParticipant()
        event_participant.event_id = request.data.get('event_id')
        event_participant.uid = request.data.get('uid')
        event_participant.stage = request.data.get('JOINED')
        event_participant.save()

        return Response(data={"message": "Event join successfully", "event_url": event.url}, status=status.HTTP_200_OK)


class InviteEventAPI(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        operation_description='Mời Tham gia sự kiện',
        operation_summary='Mời Tham gia sự kiện',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "event_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                "uid": openapi.Schema(type=openapi.TYPE_INTEGER),
                "inviter_id": openapi.Schema(type=openapi.TYPE_INTEGER),
            }
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='', examples={
                    "status": "Update successfully"
                }
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description='', examples={
                    "status": "Event not found",
                }
            )
        }
    )
    def post(self, request, *args, **kwargs): 
        try:
            event = Event.objects.get(id=request.data.get('event_id'))
        except Event.DoesNotExist:
            return Response(data={"Missing param event_id"}, status=status.HTTP_400_BAD_REQUEST)

        event_participant = EventParticipant()
        event_participant.event_id = request.data.get('event_id')
        event_participant.uid = request.data.get('uid')
        event_participant.inviter_id = request.data.get('inviter_id')
        event_participant.stage = request.data.get('INVITED')
        event_participant.save()

        # Todo mời tham gia sự kiện

        return Response(data={"message": "Event invited successfully", "event_url": event.url}, status=status.HTTP_200_OK)