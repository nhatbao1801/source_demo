import json

from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework_simplejwt.authentication import JWTAuthentication

from event.schemas.event_out_schema import EventOutSchema
from event.serializers import EventSerializer, EventParticipantSerializer
from event.serializers.event_category_serializer import EventCategorySerializer
from event.serializers.event_participant_serializer import EventOutParticipantSerializer
from event.serializers.event_serializer import EventOutSerializer
from event.serializers.event_sponsor_serializer import EventSponsorSerializer, EventSponsorOutSerializer
from hSchool.views.set_data_views_001 import SchemaBase
from models import Ticket, Event, EventParticipant, User, SponsorEvent, EventCategory
from main.serializers import TicketSerializer
from utils import none_any, name_of_none_args, convert_str_date_datetime
from utils.h_paginator import h_paginator


class TicketViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication, TokenAuthentication]
    permissions_classes = [IsAuthenticated]
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    @swagger_auto_schema(
        operation_summary='Danh sách ticket',
        operation_description='Danh sách ticket',
        manual_parameters=[
            openapi.Parameter('team_id', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Team id'),
            openapi.Parameter('org_id', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='ORG id'),
            openapi.Parameter('user_id', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='User id'),
            openapi.Parameter('page', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Trang hiện tại'),
            openapi.Parameter('limit', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='Giới hạn kết quả trên mỗi trang')
        ],
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'data': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={

                            }
                        )
                    ),
                    "metadata": SchemaBase.metadata,
                }
            )
        }
    )
    def list(self, request):
        if not request.query_params.get('team_id') and not request.query_params.get('org_id'):
            return Response(data={'status': 'Failed', 'message': 'Missing team_id and org_id'})
        try:
            queryset = Ticket.objects.all()
            event_qs = Event.objects.all()
            if request.query_params.get('team_id'):
                event_qs = event_qs.filter(team_id=request.query_params.get('team_id'))
            if request.query_params.get('org_id'):
                event_qs = event_qs.filter(organization_id=request.query_params.get('org_id'))
            event_qs = event_qs.values_list('id', flat=True)
            queryset = queryset.filter(event_id__in=event_qs)
            # if request.
            current_page, metadata = h_paginator(object_list=queryset, request=request)
            queryset_serializer = TicketSerializer(current_page, many=True, context={'request': request})
            return Response(data={'data': queryset_serializer.data, 'metadata': metadata}, status=status.HTTP_200_OK)
        except (Ticket.DoesNotExist, Exception) as e:
            if len(e.args) == 2:
                msg, code = e.args
            else:
                msg, code = e.args, None
            return Response(data={'status': f'{msg}'},
                            status=code if code is not None else HTTP_404_NOT_FOUND)


class EventViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication, TokenAuthentication]
    permissions_classes = [IsAuthenticated]
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    @swagger_auto_schema(
        operation_summary='Danh sách event',
        operation_description='Danh sách event',
        manual_parameters=[
            openapi.Parameter('team_id', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Team id'),
            openapi.Parameter('org_id', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='ORG id'),
            openapi.Parameter('is_mine', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='is mine'),
            openapi.Parameter('name', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Search by name'),
            openapi.Parameter('areas', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description='Array id của area -> [id1, id2, ...] -> Search by areas'),
            openapi.Parameter('city', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='id của thành phố thổ chức sự kiện -> Search by location'),
            openapi.Parameter('date', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description='Array dates -> [min_date, max_date] -> Search by date'),
            openapi.Parameter('type', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Search by type'),
            openapi.Parameter('price_ticket', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description='Mức giá của vé -> [min_price, max_price] -> Search by price'),
            openapi.Parameter('user_id', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='user id'),
            openapi.Parameter('is_participant', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='is_mine'),
            openapi.Parameter('page', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Trang hiện tại'),
            openapi.Parameter('limit', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='Giới hạn kết quả trên mỗi trang')
        ],
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'data': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=EventOutSchema.get_schema()
                    ),
                    "metadata": SchemaBase.metadata,
                }
            )
        }
    )
    def list(self, request):
        try:
            queryset = Event.objects.filter(application__applicationform__is_used=True)
            if request.query_params.get('name'):
                queryset = queryset.filter(name__icontains=request.query_params.get('name'))
            if request.GET.getlist('areas'):
                areas = json.loads(request.GET.get('areas'))
                queryset = queryset.filter(areas__id__in=areas)
            if request.query_params.get('city'):
                queryset = queryset.filter(city__id=request.query_params.get('city'))
            if request.query_params.get('date'):
                date = json.loads(request.GET.get('date'))
                queryset = queryset.filter(from_date__gte=convert_str_date_datetime(date[0]),
                                           from_date__lte=convert_str_date_datetime(date[1]))
            if request.query_params.get('type'):
                queryset = queryset.filter(type_id=request.query_params.get('type'))
            if request.query_params.get('price_ticket'):
                price_ticket = json.loads(request.GET.get('price_ticket'))
                ids_event = set(Ticket.objects.filter(
                    price__gte=price_ticket[0],
                    price__lte=price_ticket[1]).values_list('event_id', flat=True))
                queryset = queryset.filter(id__in=ids_event)
            if request.query_params.get('team_id'):
                queryset = Event.objects.filter(team_id=request.query_params.get('team_id'))
            if request.query_params.get('org_id'):
                queryset = Event.objects.filter(organization_id=request.query_params.get('org_id'))
            if request.query_params.get('is_mine'):
                my_team_ids = request.user.team_set.all().values_list('id')
                my_org_ids = request.user.organization_set.all().values_list('id')
                if json.loads(request.query_params.get('is_mine')):
                    queryset = Event.objects.filter(Q(team_id__in=my_team_ids) | Q(organization_id__in=my_org_ids))
            if request.query_params.get('is_participant'):
                my_team_ids = request.user.team_set.all().values_list('id')
                if json.loads(request.query_params.get('is_participant')):
                    queryset = Event.objects.filter(
                        Q(eventparticipant__team__id__in=my_team_ids) | Q(eventparticipant__user__id=request.user.id))
            if request.query_params.get('user_id'):
                _user = User.objects.get(id=request.query_params.get('user_id'))
                _team_ids = _user.team_set.all().values_list('id')
                _org_ids = _user.organization_set.all().values_list('id')
                queryset = Event.objects.filter(Q(team_id__in=_team_ids) | Q(organization_id__in=_org_ids))
            current_page, metadata = h_paginator(object_list=queryset, request=request)
            queryset_serializer = EventOutSerializer(current_page, many=True, context={'request': request})
            return Response(data={'data': queryset_serializer.data, 'metadata': metadata}, status=status.HTTP_200_OK)
        except (Event.DoesNotExist, User.DoesNotExist, Exception) as e:
            if len(e.args) == 2:
                msg, code = e.args
            else:
                msg, code = e.args, None
            return Response(data={'status': f'{msg}'},
                            status=code if code is not None else HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary='Chi tiết event',
        operation_description='Chi tiết event',
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='', schema=EventOutSchema.get_schema()
            ),
        }
    )
    def retrieve(self, request, pk=None):
        try:
            return Response(
                data={'data': EventOutSerializer(Event.objects.get(pk=pk), context={'request': request}).data},
                status=status.HTTP_200_OK)
        except (Event.DoesNotExist, Exception) as e:
            if len(e.args) == 2:
                msg, code = e.args
            else:
                msg, code = e.args, None
            return Response(data={'status': f'{msg}'},
                            status=code if code is not None else HTTP_404_NOT_FOUND)


class EventParticipantModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication, TokenAuthentication]
    permissions_classes = [IsAuthenticated]
    queryset = EventParticipant.objects.all()
    serializer_class = EventParticipantSerializer

    @swagger_auto_schema(
        operation_summary='Danh sách event participant',
        operation_description='Danh sách event participant',
        manual_parameters=[
            openapi.Parameter('is_mine', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='is mine'),
            openapi.Parameter('page', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Trang hiện tại'),
            openapi.Parameter('limit', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='Giới hạn kết quả trên mỗi trang')
        ],
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'data': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={

                            }
                        )
                    ),
                    "metadata": SchemaBase.metadata,
                }
            )
        }
    )
    def list(self, request):
        try:
            queryset = EventParticipant.objects.all()
            if request.query_params.get('is_mine'):
                my_team_ids = request.user.team_set.all().values_list('id')
                if json.loads(request.query_params.get('is_mine')):
                    queryset = queryset.filter(Q(team_id__in=my_team_ids) | Q(user_id=request.user.id))
            current_page, metadata = h_paginator(object_list=queryset, request=request)
            queryset_serializer = EventOutParticipantSerializer(current_page, many=True, context={'request': request})
            return Response(data={'data': queryset_serializer.data, 'metadata': metadata}, status=status.HTTP_200_OK)
        except (EventParticipant.DoesNotExist, Exception) as e:
            if len(e.args) == 2:
                msg, code = e.args
            else:
                msg, code = e.args, None
            return Response(data={'status': f'{msg}'},
                            status=code if code is not None else HTTP_404_NOT_FOUND)


class EventSponsorModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = SponsorEvent.objects.all()
    serializer_class = EventSponsorSerializer

    def list(self, request, *args, **kwargs):
        data, metadata = h_paginator(object_list=SponsorEvent.objects.all(), request=request)
        serializer_data = EventSponsorOutSerializer(data, many=True, context={'request': request}).data
        return Response(data={'data': serializer_data, 'metadata': metadata}, status=HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            event_sponsor = SponsorEvent.objects.get(id=pk)
            return Response(data=EventSponsorOutSerializer(event_sponsor, context={'request': request}).data,
                            status=HTTP_200_OK)
        except (SponsorEvent.DoesNotExist, Exception) as e:
            if len(e.args) == 2:
                msg, code = e.args
            else:
                msg, code = e.args, None
            return Response(data={'status': 'Failed', 'message': f'{msg}'},
                            status=code if code is not None else HTTP_404_NOT_FOUND)


class EventCategoryModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = EventCategory.objects.all()
    serializer_class = EventCategorySerializer
