import logging

from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
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
        _serializer = self.get_serializer_class()
        _queryset = EventParticipant.objects.filter(is_deleted=False, event_id=request.GET.get('event_id'))
        data, metadata = s_paginator(object_list=_queryset, request=request)
        data_serializer = _serializer(data, many=True, context={'request': request}).data
        return JsonResponse(
            data={
                'data': data_serializer,
                'metadata': metadata
            }, status=status.HTTP_200_OK
        )


    @swagger_auto_schema(
        operation_summary='Xóa participant', tags=['event']
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

        is_joined = EventParticipant.objects.filter(uid_id=request.data.get('uid'), event_id=request.data.get('event_id'), stage='JOINED')
        if is_joined.count() > 0:
            return Response(data={"You has joined this event"}, status=status.HTTP_400_BAD_REQUEST)
            
        event_participant = EventParticipant()
        event_participant.event_id = request.data.get('event_id')
        event_participant.uid_id = request.data.get('uid')
        event_participant.stage = 'JOINED'
        event_participant.save()

        return Response(data={"message": "Event join successfully"}, status=status.HTTP_200_OK)


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
                "uid": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_INTEGER)),
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

        participants = []
        event_id = request.data.get('event_id')
        for uid in request.data.get('uid'):
            participants.append(EventParticipant({"event_id": event_id, "uid_id": uid, 'inviter_id': request.data.get('inviter_id'), "stage": 'INVITED'}))
        EventParticipant.objects.bulk_create(participants)

        # Todo mời tham gia sự kiện

        return Response(data={"message": "Event invited successfully"}, status=status.HTTP_200_OK)