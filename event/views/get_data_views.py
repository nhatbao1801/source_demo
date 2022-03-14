from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from event.serializers import EventSerializer
from event.serializers.event_type_serializer import EventTypeSerializer
from event.views.support.suggestion import get_event_near_user
from models.event import EventType, Event
from utils import data_from_method_get
from utils.h_paginator import h_paginator


class AllEventViewAPI(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description='Danh sách toàn bộ các sự kiện',
        operation_summary='Danh sách toàn bộ các sự kiện',
        manual_parameters=[
            openapi.Parameter('search', in_=openapi.IN_QUERY, description='Từ khóa để search',
                              type=openapi.TYPE_STRING),
            openapi.Parameter('team_id', in_=openapi.IN_QUERY, description='Team id',
                              type=openapi.TYPE_STRING),
            openapi.Parameter('org_id', in_=openapi.IN_QUERY, description='Org',
                              type=openapi.TYPE_STRING),
            openapi.Parameter('page', in_=openapi.IN_QUERY, description='Trang hiện tại', type=openapi.TYPE_INTEGER),
            openapi.Parameter('limit', in_=openapi.IN_QUERY, description='Số item trên mỗi trang',
                              type=openapi.TYPE_INTEGER),
        ],
        responses={
            HTTP_200_OK: openapi.Response(
                description='', schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'data': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'name': openapi.Schema(type=openapi.TYPE_STRING),
                                    'profile_pic': openapi.Schema(type=openapi.TYPE_STRING),
                                    'background': openapi.Schema(type=openapi.TYPE_STRING),
                                    'description': openapi.Schema(type=openapi.TYPE_STRING),
                                    'start_date': openapi.Schema(type=openapi.TYPE_STRING,
                                                                 format=openapi.FORMAT_DATETIME),
                                    'end_date': openapi.Schema(type=openapi.TYPE_STRING,
                                                               format=openapi.FORMAT_DATETIME),
                                    'address': openapi.Schema(type=openapi.TYPE_STRING),
                                    'modified_perm': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                                                    description='User hiện tại có quyền chỉnh sửa sự kiện không?'),
                                    'object_creation': openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            'object': openapi.Schema(type=openapi.TYPE_STRING, enum=[
                                                'organization', 'team'
                                            ]),
                                            'url': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_SLUG)
                                        }
                                    ),
                                    'city': openapi.Schema(type=openapi.TYPE_STRING),
                                    'type': openapi.Schema(type=openapi.TYPE_STRING),
                                    'date_created': openapi.Schema(type=openapi.TYPE_STRING,
                                                                   format=openapi.FORMAT_DATETIME),
                                    'picture': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI),
                                    'url': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI),
                                    'hash_tag': openapi.Schema(type=openapi.TYPE_STRING),
                                    'street_address': openapi.Schema(type=openapi.TYPE_STRING),
                                    'venue': openapi.Schema(type=openapi.TYPE_STRING),
                                    'tagline': openapi.Schema(type=openapi.TYPE_STRING),
                                    'from_date': openapi.Schema(type=openapi.TYPE_STRING,
                                                                format=openapi.FORMAT_DATETIME),
                                    'to_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                                    'schedule': openapi.Schema(type=openapi.TYPE_STRING),
                                    'last_modified': openapi.Schema(type=openapi.TYPE_STRING,
                                                                    format=openapi.FORMAT_DATETIME),
                                    'area': openapi.Schema(type=openapi.TYPE_ARRAY,
                                                           items=openapi.Schema(type=openapi.TYPE_STRING))
                                }
                            )
                        ),
                        'metadata': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "count": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "num_pages": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "page_range": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(
                                    type=openapi.TYPE_INTEGER
                                )),
                                "has_next": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                "has_previous": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                "current_page": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "next_page_number": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "previous_page_number": openapi.Schema(type=openapi.TYPE_INTEGER)
                            }
                        )
                    }
                )
            )
        }
    )
    def get(self, request, *args, **kwargs):
        search = request.query_params.get('search')
        
        org_id = request.query_params.get('org_id')
        team_id = request.query_params.get('team_id')
        events = Event.objects.all()
        if search:
            events = events.filter(name__icontains=search)
        if org_id:
            events = events.filter(organization_id=org_id)
        if team_id:
            events = events.filter(team_id=team_id)

        all_events = events.order_by('-date_created')
        events, metadata = h_paginator(all_events, request)
        response = []
        for event in events:
            res_content = {
                'id': event.id,
                'object_creation': {
                    'name': event.get_owner().name,
                    'picture': event.get_owner().get_picture_url(),
                    'url': event.get_owner().url
                },
                'city_id': event.city.id,
                'event_type_id': event.type.id,
                'name': event.name,
                'date_created': event.date_created,
                'picture': event.picture.build_url(width=200, height=200, secure=True,
                                                   crop='thumb') if event.picture is not None else None,
                'url': event.url,
                'cover': self.get_cover(event),
                'hash_tag': event.hash_tag,
                'street_address': event.street_address,
                'venue': event.venue,
                'description': event.description,
                'tagline': event.tagline,
                'from_date': event.from_date,
                'to_date': event.to_date,
                'schedule': event.schedule,
                'last_modified': event.last_modified,
                'areas_id': [ar_id.id for ar_id in event.areas.all()],
                'city_info': {"id": event.city.id, "name": event.city.name},
                'areas_info': [{"id": area.id, "name": area.name} for area in event.areas.all()],
                'type_info': {"id": event.type.id, "name": event.type.name},
            }
            response.append(res_content)
        content = {
            "data": response,
            "metadata": metadata
        }
        return Response(data=content, status=HTTP_200_OK)

    @staticmethod
    def get_cover(obj):
        media = obj.media_set.filter(Q(media_type='img') & Q(set_as_cover=True)).first()
        cover_picture = None
        if media and media.image:
            cover_picture = media.image.build_url(secure=True)
        return cover_picture


class GetAllEventNearMeAPI(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description='Danh sách toàn bộ các sự kiện gần người dùng',
        operation_summary='Danh sách toàn bộ các sự kiện gần người dùng',
        manual_parameters=[
            openapi.Parameter('search', in_=openapi.IN_QUERY, description='Từ khóa để search',
                              type=openapi.TYPE_STRING),
            openapi.Parameter('page', in_=openapi.IN_QUERY, description='Trang hiện tại', type=openapi.TYPE_INTEGER),
            openapi.Parameter('limit', in_=openapi.IN_QUERY, description='Số item trên mỗi trang',
                              type=openapi.TYPE_INTEGER),
        ],
        responses={
            HTTP_200_OK: openapi.Response(
                description='', schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'data': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'title': openapi.Schema(type=openapi.TYPE_STRING),
                                    'profile_pic': openapi.Schema(type=openapi.TYPE_STRING),
                                    'background': openapi.Schema(type=openapi.TYPE_STRING),
                                    'description': openapi.Schema(type=openapi.TYPE_STRING),
                                    'start_date': openapi.Schema(type=openapi.TYPE_STRING,
                                                                 format=openapi.FORMAT_DATETIME),
                                    'end_date': openapi.Schema(type=openapi.TYPE_STRING,
                                                               format=openapi.FORMAT_DATETIME),
                                    'address': openapi.Schema(type=openapi.TYPE_STRING),
                                    'url': openapi.Schema(type=openapi.TYPE_STRING),
                                    'modified_perm': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                                                    description='User hiện tại có quyền chỉnh sửa sự kiện không?'),
                                }
                            )
                        ),
                        'metadata': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "count": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "num_pages": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "page_range": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(
                                    type=openapi.TYPE_INTEGER
                                )),
                                "has_next": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                "has_previous": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                "current_page": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "next_page_number": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "previous_page_number": openapi.Schema(type=openapi.TYPE_INTEGER)
                            }
                        )
                    }
                )
            )
        }
    )
    def get(self, request, *args, **kwargs):
        all_events_near_me = get_event_near_user(request)
        events_near_me, metadata = h_paginator(all_events_near_me, request)
        response = []
        for event in events_near_me:
            background = event.picture.build_url(secure=True, width=237, height=178,
                                                 crop='thumb') if event.picture is not None else None
            des = event.description
            res_content = {
                'id': event.id,
                'name': event.name,
                'profile_pic': event.picture.build_url(width=200, height=200, secure=True,
                                                       crop='thumb') if event.picture is not None else None,
                'background': background,
                'description': des,
                'start_date': event.from_date.strftime("%d/%m/%Y - %H:%M") if event.from_date else None,
                'end_date': event.to_date.strftime("%d/%m/%Y - %H:%M") if event.to_date else None,
                'address': event.street_address if event.street_address else '',
                'url': event.url,
                'modified_perm': request.user.id == event.get_owner().user.id
            }
            response.append(res_content)
        content = {
            "data": response,
            "metadata": metadata
        }
        return Response(data=content, status=HTTP_200_OK)


class GetEventTypes(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description='Danh sách các loại sự kiện',
        operation_summary='Danh sách các loại sự kiện',
        manual_parameters=[
            openapi.Parameter('page', in_=openapi.IN_QUERY, description='Trang hiện tại', type=openapi.TYPE_INTEGER),
            openapi.Parameter('limit', in_=openapi.IN_QUERY, description='Số item trên mỗi trang',
                              type=openapi.TYPE_INTEGER)
        ],
        responses={
            HTTP_200_OK: openapi.Response(
                description='', schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'data': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'name': openapi.Schema(type=openapi.TYPE_STRING),
                            }
                        )),
                        'metadata': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "count": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "num_pages": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "page_range": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(
                                    type=openapi.TYPE_INTEGER
                                )),
                                "has_next": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                "has_previous": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                "current_page": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "next_page_number": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "previous_page_number": openapi.Schema(type=openapi.TYPE_INTEGER)
                            }
                        )
                    }
                )
            )
        }
    )
    def get(self, request, *args, **kwargs):
        query = EventType.objects.all()
        count_pagination = query.count()
        if not request.GET.get('limit'):
            if not request.GET._mutable:
                request.GET._mutable = True
            request.GET['limit'] = count_pagination
        event_types, metadata = h_paginator(query, request)
        content = {
            "data": EventTypeSerializer(event_types, many=True).data,
            "metadata": metadata
        }
        return Response(data=content, status=HTTP_200_OK)


class EventFilterBy(APIView):

    @swagger_auto_schema(
        operation_summary='Lọc danh sách sự kiện theo team hoặc tổ chức',
        operation_description='Lọc danh sách sự kiện theo team hoặc tổ chức',
        manual_parameters=[
            openapi.Parameter('by', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, enum=['team', 'org']),
            openapi.Parameter('id', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='team id | org id')
        ],
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'areas': openapi.Schema(type=openapi.TYPE_ARRAY,
                                                items=openapi.Schema(type=openapi.TYPE_STRING)),
                        'name': openapi.Schema(type=openapi.TYPE_STRING),
                        'date_created': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                        'picture': openapi.Schema(type=openapi.TYPE_STRING),
                        'picture_url': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI),
                        'url': openapi.Schema(type=openapi.TYPE_STRING),
                        'hash_tag': openapi.Schema(type=openapi.TYPE_STRING),
                        'street_address': openapi.Schema(type=openapi.TYPE_STRING),
                        'venue': openapi.Schema(type=openapi.TYPE_STRING),
                        'tagline': openapi.Schema(type=openapi.TYPE_STRING),
                        'description': openapi.Schema(type=openapi.TYPE_STRING),
                        'from_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                        'to_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                        'schedule': openapi.Schema(type=openapi.TYPE_STRING),
                        'last_modified': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                        'team': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'unique_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'name': openapi.Schema(type=openapi.TYPE_STRING),
                                'picture': openapi.Schema(type=openapi.TYPE_STRING),
                                'picture_url': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI),
                                'url': openapi.Schema(type=openapi.TYPE_STRING),
                                'founded_date': openapi.Schema(type=openapi.TYPE_STRING,
                                                               format=openapi.FORMAT_DATETIME),
                                'tagline': openapi.Schema(type=openapi.TYPE_STRING),
                                'android_app_link': openapi.Schema(type=openapi.TYPE_STRING),
                                'ios_app_link': openapi.Schema(type=openapi.TYPE_STRING),
                                'description': openapi.Schema(type=openapi.TYPE_STRING),
                                'is_startup': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                'vision': openapi.Schema(type=openapi.TYPE_STRING),
                                'mission': openapi.Schema(type=openapi.TYPE_STRING),
                                'core_value': openapi.Schema(type=openapi.TYPE_STRING),
                                'phone_num': openapi.Schema(type=openapi.TYPE_STRING),
                                'street_address': openapi.Schema(type=openapi.TYPE_STRING),
                                'last_modified': openapi.Schema(type=openapi.TYPE_STRING,
                                                                format=openapi.FORMAT_DATETIME),
                                'use_for_studying': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                'user': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'stage': openapi.Schema(type=openapi.TYPE_INTEGER)
                            },
                            description='null trong trường hợp event do organization tạo'
                        ),
                        'organization': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'unique_id': openapi.Schema(type=openapi.TYPE_STRING),
                                'name': openapi.Schema(type=openapi.TYPE_STRING),
                                'picture': openapi.Schema(type=openapi.TYPE_STRING),
                                'picture_url': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI),
                                'street_address': openapi.Schema(type=openapi.TYPE_STRING),
                                'url': openapi.Schema(type=openapi.TYPE_STRING),
                                'tagline': openapi.Schema(type=openapi.TYPE_STRING),
                                'description': openapi.Schema(type=openapi.TYPE_STRING),
                                'last_modified': openapi.Schema(type=openapi.TYPE_STRING,
                                                                format=openapi.FORMAT_DATETIME),
                                'user': openapi.Schema(type=openapi.TYPE_STRING),
                                'type': openapi.Schema(type=openapi.TYPE_STRING),
                                'city': openapi.Schema(type=openapi.TYPE_STRING)
                            },
                            description='null trong trường hợp event do team tạo'
                        ),
                        'city': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'name': openapi.Schema(type=openapi.TYPE_STRING),
                                    'country': openapi.Schema(type=openapi.TYPE_INTEGER),
                                }
                            )
                        ),
                        'type': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'name': openapi.Schema(type=openapi.TYPE_STRING),
                            }
                        )
                    }
                )
            )
        }
    )
    def get(self, request):
        _by, _id = data_from_method_get(request, 'by', 'id')
        if _by == 'team':
            events = Event.objects.filter(team_id=_id)
            current_page, metadata = h_paginator(events, request)
            events_serializer = EventSerializer(current_page.object_list, many=True)
            return Response(data={'data': events_serializer.data, 'metadata': metadata})
        if _by == 'org':
            events = Event.objects.filter(organization_id=_id)
            current_page, metadata = h_paginator(events, request)
            events_serializer = EventSerializer(current_page.object_list, many=True)
            return Response(data={'data': events_serializer.data, 'metadata': metadata})
        return Response(data={'status': 'key by must be either team or org'}, status=status.HTTP_400_BAD_REQUEST)
