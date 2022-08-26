import logging
from datetime import datetime
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from event.serializers.event_participant_serializer import EventListInviteSchema
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
from django.db.models import Q

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
            openapi.Parameter(
                'nolimit', type=openapi.TYPE_BOOLEAN, in_=openapi.IN_QUERY,
                description='Nolimit', default=False
            ),
            openapi.Parameter(
                'search', type=openapi.TYPE_STRING, in_=openapi.IN_QUERY,
                description='Search'
            ),
            openapi.Parameter(
                'date_from', type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, in_=openapi.IN_QUERY,
                description='Date from'
            ),
            openapi.Parameter(
                'date_to', type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, in_=openapi.IN_QUERY,
                description='Date to'
            ),
            openapi.Parameter(
                'is_invited', type=openapi.TYPE_BOOLEAN, in_=openapi.IN_QUERY,
                description='is_invited'
            ),
            openapi.Parameter(
                'is_host', type=openapi.TYPE_BOOLEAN, in_=openapi.IN_QUERY,
                description='is_host'
            ),
            openapi.Parameter(
                'is_joined', type=openapi.TYPE_BOOLEAN, in_=openapi.IN_QUERY,
                description='is_joined'
            ),
            openapi.Parameter(
                'date_out', type=openapi.TYPE_BOOLEAN, in_=openapi.IN_QUERY,
                description='date_out'
            ),
            openapi.Parameter(
                'formality_id', type=openapi.TYPE_INTEGER, in_=openapi.IN_QUERY,
                description='formality_id'
            ),
            openapi.Parameter(
                'privacy_id', type=openapi.TYPE_INTEGER, in_=openapi.IN_QUERY,
                description='privacy_id'
            ),openapi.Parameter(
                'business_level_code', type=openapi.TYPE_STRING, in_=openapi.IN_QUERY,
                description='business_level_code'
            ),
        ], paginator_inspectors=[PaginatorInspectorClass], tags=['event']
    )
    @method_decorator(cache_page(3))
    def list(self, request, *args, **kwargs):
        _serializer = self.get_serializer_class()
        search = self.request.GET.get('search')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        is_invited = self.request.GET.get('is_invited')
        is_host = self.request.GET.get('is_host')
        is_joined = self.request.GET.get('is_joined')
        date_out = self.request.GET.get('date_out')
        uid = self.request.GET.get('uid')
        formality_id = self.request.GET.get('formality_id')
        privacy_id = self.request.GET.get('privacy_id')
        business_level_code = self.request.GET.get('business_level_code')

        _queryset = Event.objects.filter()
        if not is_host:
            _queryset = _queryset.filter(~Q(privacy__code="PRIVATE"))
        if search:
            _queryset = _queryset.filter(name__icontains=search)
        if date_from and date_to:
            _queryset = _queryset.filter(Q(from_date__gte=date_from), Q(to_date__lte=date_to))
        elif date_from:
             _queryset = _queryset.filter(from_date__gte=date_from)
        elif date_to:
             _queryset = _queryset.filter(to_date__gte=date_to)
        if is_invited:
            _queryset = _queryset.filter(Q(eventparticipant__inviter_id__isnull=False), Q(eventparticipant__uid=uid))
        if is_host:
            _queryset = _queryset.filter(owner=uid)
        if is_joined:
            _queryset = _queryset.filter(Q(eventparticipant__uid=uid), Q(stage="JOINED"))
        if date_out:
            now = datetime.today().isoformat()
            _queryset = _queryset.filter(to_date__lt=now)
        if formality_id:
            _queryset = _queryset.filter(formality_id=formality_id)
        if privacy_id:
            _queryset = _queryset.filter(privacy_id=privacy_id)
        if business_level_code:
            _queryset = _queryset.filter(business_level_code=business_level_code)
        _queryset = _queryset.order_by('-from_date')
        data, metadata = s_paginator(object_list=_queryset, request=request)
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
        instance = self.get_object()
        serializer = self.get_serializer_class()
        _serializer = serializer(instance, many=False, context={'request': request})
        return Response(_serializer.data)

    
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

        is_joined = EventParticipant.objects.filter(uid=request.data.get('uid'), event_id=request.data.get('event_id'), stage='JOINED')
        if is_joined.count() > 0:
            return Response(data={"You has joined this event"}, status=status.HTTP_400_BAD_REQUEST)
        
        # EventParticipant.objects.filter(uid=request.data.get('uid'), event_id=request.data.get('event_id')).update(stage='JOINED')
        EventParticipant.objects.update_or_create(uid=request.data.get('uid'), event_id=request.data.get('event_id'), defaults={"stage": "JOINED"})
        # event_participant = EventParticipant()
        # event_participant.event_id = request.data.get('event_id')
        # event_participant.uid = request.data.get('uid')
        # event_participant.stage = 'JOINED'
        # event_participant.save()

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
                "uid": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
                "inviter_id": openapi.Schema(type=openapi.TYPE_STRING),
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
            if EventParticipant.objects.filter(event_id=event_id, uid=uid, inviter_id=request.data.get('inviter_id')).count() <= 0:
                participants.append(EventParticipant(event_id=event_id, uid=uid, inviter_id=request.data.get('inviter_id'), stage='INVITED'))
        if len(participants) <= 0:
            return Response(data={"message": "Uids đã được mời vào rồi"}, status=status.HTTP_400_BAD_REQUEST)
        EventParticipant.objects.bulk_create(participants)
        return Response(data={"message": "Event invited successfully"}, status=status.HTTP_200_OK)

class EventStatisticsAPI(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        operation_description='Thống kê sự kiện',
        operation_summary='Thống kê sự kiện',
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='', examples={
                    "data": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "event_count": openapi.Schema(type=openapi.TYPE_INTEGER),
                            "event_passed_count": openapi.Schema(type=openapi.TYPE_INTEGER),
                            "event_member_count": openapi.Schema(type=openapi.TYPE_INTEGER)
                        }
                    )
                }
            )
        }
    )
    def get(self, request, *args, **kwargs):
        events = Event.objects.all()
        event_count = events.count()

        now = datetime.today().isoformat()
        passed_event = events.filter(to_date__lt=now)
        event_passed_count = passed_event.count()

        participants = EventParticipant.objects.count()
        _data = {
            "event_count": event_count,
            "event_passed_count": event_passed_count,
            "event_member_count": participants
        }
        return Response(data={"data": _data}, status=status.HTTP_200_OK)


class ListInviteEventAPI(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        operation_description='Danh sách lời mời tham gia',
        operation_summary='Danh sách lời mời tham gia',
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='', examples={
                    "data": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "test": openapi.Schema(type=openapi.TYPE_STRING)
                        }
                    )
                }
            )
        }
    )
    def get(self, request, *args, **kwargs):
        uid = request.query_params.get('uid')
        list_invite_join = EventParticipant.objects.filter(uid=uid, stage='INVITED')
        _serializer = EventListInviteSchema
        data, metadata = s_paginator(object_list=list_invite_join, request=request)
        data_serializer = _serializer(data, many=True, context={'request': request}).data
        return JsonResponse(
            data={
                'data': data_serializer,
                'metadata': metadata
            }, status=status.HTTP_200_OK
        )
