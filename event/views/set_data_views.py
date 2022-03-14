########################################################################################################################
#                                                   CLASS BASED VIEWS SECTION                                          #
########################################################################################################################
import json

import cloudinary.api
from django.core.files import File
from django.db.models import Q
from django.db.utils import IntegrityError
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_404_NOT_FOUND,
                                   HTTP_403_FORBIDDEN)
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from event.models.post import Post
from event.models.team import Team
from event.serializers.event_serializer import EventOutSerializer, EventSerializer
from event.serializers.post_serializer import PostSerializer

from event.views.support.send_email import owner_event_send_thanks, team_or_user_send_join_event
from event.models.event import Event
from event.models.media import Media
from event.models.event_participant import EventParticipant
from event.models.area import Area
from utils import update_cover, data_from_method_post_put_delete, convert_str_date_datetime


class AddEventAPI(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description='Tạo sự kiện',
        operation_summary='Tạo sự kiện',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'owner_id': openapi.Schema(type=openapi.TYPE_INTEGER,
                                           description='ID của đối tượng tạo event, phụ thuộc vào owner_type,'
                                                       'với owner_type là team thì này là của team và tương tự với owner type khác'),
                'owner_type': openapi.Schema(type=openapi.TYPE_STRING, description='Xác định đối tượng tạo event',
                                             enum=['org', 'team']),
                'city_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID thành phố'),
                'areas_id': openapi.Schema(type=openapi.TYPE_STRING,
                                           description='ID công nghệ và lĩnh vực công nghệ [1, 2, 3,...]'),
                'event_type_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Loại event'),
                'name': openapi.Schema(type=openapi.TYPE_INTEGER, description='Tên event'),
                'from_date': openapi.Schema(type=openapi.TYPE_STRING, description='Ngày bắt đầu',
                                            format=openapi.FORMAT_DATETIME),
                'to_date': openapi.Schema(type=openapi.TYPE_STRING, description='Ngày kết thúc',
                                          format=openapi.FORMAT_DATETIME),
                'picture': openapi.Schema(type=openapi.TYPE_FILE, description='Ảnh của event',
                                          format=openapi.FORMAT_BINARY),
                'hash_tag': openapi.Schema(type=openapi.TYPE_STRING, description='Tag tìm kiếm event trên MXH khác'),
                'street_address': openapi.Schema(type=openapi.TYPE_STRING, description='Địa chỉ cụ thể của event'),
                'venue': openapi.Schema(type=openapi.TYPE_STRING, description='Tên địa điểm tổ chức event'),
                'tagline': openapi.Schema(type=openapi.TYPE_STRING, description='Tag giúp tìm kiếm event trong hSpace'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='Mô tả chi tiết về event'),
                'schedule': openapi.Schema(type=openapi.TYPE_STRING, description='Kế hoạch tổ chức của event'),
                'cover': openapi.Schema(type=openapi.TYPE_FILE, description='File cover của event',
                                        format=openapi.FORMAT_BINARY),
            }
        ),
        responses={
            HTTP_201_CREATED: openapi.Response(
                description='', schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status': openapi.Schema(type=openapi.TYPE_STRING, default='Created!'),
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
                        'name': openapi.Schema(type=openapi.TYPE_STRING),
                        'date_created': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                        'picture': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI),
                        'url': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI),
                        'hash_tag': openapi.Schema(type=openapi.TYPE_STRING),
                        'street_address': openapi.Schema(type=openapi.TYPE_STRING),
                        'venue': openapi.Schema(type=openapi.TYPE_STRING),
                        'tagline': openapi.Schema(type=openapi.TYPE_STRING),
                        'from_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                        'to_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                        'schedule': openapi.Schema(type=openapi.TYPE_STRING),
                        'last_modified': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                        'area': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING))
                    }
                )

            ),
            HTTP_400_BAD_REQUEST: openapi.Response(
                description='', schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status': openapi.Schema(type=openapi.TYPE_STRING, enum=[
                            'Type is not valid or null(type is must "org" or "team"',
                            'missing owner_id', 'areas_is must be a list',
                            'area_id=... is not valid or is None', 'Failed to created due to lack of needed fields',
                            '...'
                        ]),
                    }
                )
            )
        }
    )
    def post(self, request, *args, **kwargs):
        """
            **Data**
            ```js
            {
                "all_date": "boolean",                //Chưa hỗ trợ. Có thể null
                "visibility": "boolean",              //Chưa hỗ trợ. Có thể null
                "location": "string",                 //Chưa hỗ trợ. Có thể null
                "description": "string",               //Chưa hỗ trợ. Có thể null
                "show_guest": "boolean",                //Chưa hỗ trợ. Có thể null
                "only_admin_can_post": "boolean",       //Chưa hỗ trợ. Có thể null
                "host_or_cohost_approve": "boolean",    //Chưa hỗ trợ. Có thể null
            }
            ```
        """
        (owner_id, owner_type, city_id, areas_id, event_type_id, name, picture, hash_tag, street_address, venue,
         tagline, description, from_date, to_date, schedule, cover) = data_from_method_post_put_delete(
            request,
            'owner_id', 'owner_type', 'city_id', 'areas_id', 'event_type_id', 'name', 'picture', 'hash_tag',
            'street_address',
            'venue', 'tagline', 'description', 'from_date', 'to_date', 'schedule', 'cover'
        )
        # check object creation event
        if owner_id:
            if str(owner_type).strip() == 'org':
                organization_id = owner_id
                team_id = None
            elif str(owner_type).strip() == 'team':
                organization_id = None
                team_id = owner_id
            else:
                return Response(data={'status': 'Type is not valid or null(type is must "org" or "team"'},
                                status=HTTP_400_BAD_REQUEST)
        else:
            return Response(data={'status': 'missing owner_id'}, status=HTTP_400_BAD_REQUEST)

        event_serializer = EventSerializer(data={
            'team': team_id, 'organization': organization_id, 'city': city_id, 'type': event_type_id, 'name': name,
            'picture': picture, 'hash_tag': hash_tag, 'street_address': street_address, 'venue': venue,
            'tagline': tagline, 'description': description, 'from_date': from_date, 'to_date': to_date,
            'schedule': schedule, 'created_by': request.user.id
        })
        if event_serializer.is_valid():
            if areas_id:
                areas_id = json.loads(areas_id)
                if not isinstance(areas_id, list):
                    return Response(data={'status': 'areas_is must be a stringify of a list'},
                                    status=HTTP_400_BAD_REQUEST)
            event = event_serializer.save()
            Media.objects.create(event_id=event.id, media_type='img', image=cover,
                                 set_as_cover=True)
            if areas_id:
                for area_id in areas_id:
                    try:
                        event.areas.add(Area.objects.get(id=area_id))
                    except IntegrityError:
                        return Response(data={'status': f'area_id={area_id} is not valid or is None'},
                                        status=HTTP_400_BAD_REQUEST)
            return Response(
                data={"status": "Created", "data": EventOutSerializer(event, context={'request': request}).data},
                status=HTTP_201_CREATED
            )
        else:
            return Response(data=event_serializer.errors, status=HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_cover(obj):
        media = obj.media_set.filter(Q(media_type='img') & Q(set_as_cover=True)).first()
        cover_picture = None
        if media and media.image:
            cover_picture = media.image.build_url(secure=True)
        return cover_picture


class EditEventAPI(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description='Cập nhật sự kiện',
        operation_summary='Cập nhật sự kiện',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'event_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID sự kiện'),
                'city_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID thành phố'),
                'areas_id': openapi.Schema(type=openapi.TYPE_STRING,
                                           description='ID công nghệ và lĩnh vực công nghệ [1, 2, 3,...]'),
                'event_type_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Loại event'),
                'name': openapi.Schema(type=openapi.TYPE_INTEGER, description='Tên event'),
                'from_date': openapi.Schema(type=openapi.TYPE_STRING, description='Ngày bắt đầu',
                                            format=openapi.FORMAT_DATETIME),
                'to_date': openapi.Schema(type=openapi.TYPE_STRING, description='Ngày kết thúc',
                                          format=openapi.FORMAT_DATETIME),
                'hash_tag': openapi.Schema(type=openapi.TYPE_STRING, description='Tag tìm kiếm event trên MXH khác'),
                'street_address': openapi.Schema(type=openapi.TYPE_STRING, description='Địa chỉ cụ thể của event'),
                'url': openapi.Schema(type=openapi.TYPE_STRING, description='Url tùy chỉnh của event'),
                'venue': openapi.Schema(type=openapi.TYPE_STRING, description='Tên địa điểm tổ chức event'),
                'tagline': openapi.Schema(type=openapi.TYPE_STRING, description='Tag giúp tìm kiếm event trong hSpace'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='Mô tả chi tiết về event'),
                'schedule': openapi.Schema(type=openapi.TYPE_STRING, description='Kế hoạch tổ chức của event'),
                'picture': openapi.Schema(type=openapi.TYPE_STRING, description=''),
                'cover': openapi.Schema(type=openapi.TYPE_STRING, description=''),
            }
        ),
        responses={
            HTTP_200_OK: openapi.Response(
                description='', schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status': openapi.Schema(type=openapi.TYPE_STRING, default='Event created successfully'),
                        'event_url': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_SLUG)
                    }
                )
            ),
            HTTP_400_BAD_REQUEST: openapi.Response(
                description='', examples={
                    "status": "Missing param event_id",
                    '...': '...'
                }
            ),
            HTTP_404_NOT_FOUND: openapi.Response(
                description='', examples={
                    "status": "Event could not be found"
                }
            )
        }
    )
    def put(self, request, *args, **kwargs):
        (event_id, city_id, areas_id, event_type_id, name, hash_tag, street_address, url, venue,
         tagline, description, from_date, to_date, schedule, picture, cover) = data_from_method_post_put_delete(
            request,
            'event_id', 'city_id', 'areas_id', 'event_type_id', 'name', 'hash_tag',
            'street_address', 'url',
            'venue', 'tagline', 'description', 'from_date', 'to_date', 'schedule', 'picture', 'cover'
        )

        if event_id is None:
            return Response(data={'status': 'Missing event_id'}, status=HTTP_400_BAD_REQUEST)
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response(data={"status": "Event could not be found"}, status=HTTP_404_NOT_FOUND)

        data_put = {
            'created_by': request.user.id, 'hash_tag': hash_tag, 'name': name, 'street_address': street_address,
            'city': city_id, 'type': event_type_id, 'from_date': from_date, 'to_date': to_date,
            'description': description,
            'venue': venue, 'schedule': schedule, 'tagline': tagline
        }
        if url:
            data_put['url'] = url

        event_serializer = EventSerializer(data=data_put, instance=event, partial=True)
        if event_serializer.is_valid():
            event_serializer.save()
            if areas_id:
                areas_id = json.loads(areas_id)
                event.areas.clear()
                for area_id in areas_id:
                    # add areas
                    try:
                        event.areas.add(Area.objects.get(id=area_id))
                    except IntegrityError:
                        return Response(data={'status': f'area_id={area_id} is not valid or is None'},
                                        status=HTTP_400_BAD_REQUEST)
            if not isinstance(areas_id, list):
                return Response(data={'status': 'areas_is must be a list'}, status=HTTP_400_BAD_REQUEST)
            if picture:
                if isinstance(picture, File) and picture.size == 0:
                    return Response(data={'status': 'picture is empty'}, status=HTTP_400_BAD_REQUEST)
                if event.picture is not None:
                    cloudinary.api.delete_resources(event.picture.public_id)
                event.picture = picture
                event.save()
                event.picture_url = event.picture.build_url() if event.picture is not None else None
                event.save()
            if cover:
                medias = Media.objects.filter(Q(event=event) & Q(set_as_cover=True))
                if medias.exists():
                    try:
                        for m in medias:
                            if m.media_type == 'img' and m.image is not None:
                                cloudinary.api.delete_resources(m.image.public_id)
                                m.image = None
                            elif m.media_type == 'vid':
                                m.url = None
                                m.media_type = 'img'
                            m.delete()
                    except Exception:
                        pass
                media = Media.objects.create(event=event, image=cover, set_as_cover=True,
                                             media_type='img')

        else:
            return Response(data=event_serializer.errors, status=HTTP_400_BAD_REQUEST)
        if event:
            return Response(data={
                "status": "updated!",
                "data": EventOutSerializer(Event.objects.get(pk=event.pk), context={'request': request}).data},
                status=HTTP_200_OK)
        else:
            return Response(data={"status": "Missing param event_id"}, status=HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_cover(obj):
        media = obj.media_set.filter(Q(media_type='img') & Q(set_as_cover=True)).first()
        cover_picture = None
        if media and media.image:
            cover_picture = media.image.build_url(secure=True)
        return cover_picture


class DeleteEvent(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description='Xóa sự kiện',
        operation_summary='Xóa sự kiện',
        manual_parameters=[
            openapi.Parameter('id', in_=openapi.IN_PATH, description='Id của sự kiện', type=openapi.TYPE_INTEGER)
        ],
        responses={
            HTTP_200_OK: openapi.Response(
                description='', examples={
                    'status': 'Deleted'
                }
            ),
            HTTP_403_FORBIDDEN: openapi.Response(
                description='', examples={
                    'status': 'Failed',
                    'message': 'Permission Denied'
                }
            ),
            HTTP_404_NOT_FOUND: openapi.Response(
                description='', examples={
                    'status': 'Not found'
                }
            )
        }
    )
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('id')
        try:
            event = Event.objects.get(pk=pk)
            # CHeck if event's owner is current user sent the request
            if request.user.id != event.get_owner().user.id:
                return Response(data={'status': 'Failed', 'message': 'Permission Denied'}, status=HTTP_403_FORBIDDEN)
            event.delete()
            return Response(data={'status': 'Deleted'}, status=HTTP_200_OK)
        except (Event.DoesNotExist, Exception):
            return Response(data={'status': 'Not found'}, status=HTTP_404_NOT_FOUND)


class JoinEventAPI(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description='Tham gia sự kiện',
        operation_summary='Tham gia sự kiện',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "event_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                "current_owner_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                "me_or_team_id": openapi.Schema(type=openapi.TYPE_INTEGER),
            }
        ),
        responses={
            HTTP_200_OK: openapi.Response(
                description='', examples={
                    "status": "Update successfully"
                }
            ),
            HTTP_404_NOT_FOUND: openapi.Response(
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
            return Response(data={"Missing param event_id"}, status=HTTP_400_BAD_REQUEST)

        team_id = request.data.get('me_or_team_id')

        # participant
        participant = EventParticipant()
        participant.event_id = event.id
        if team_id:
            try:
                team = Team.objects.get(pk=team_id)
            except Team.DoesNotExist:
                return Response(data={"Event not found"}, status=HTTP_404_NOT_FOUND)
            owner_team_mail = team.user.email
            team_or_user_name = team.name
            participant.team_id = team_id
        else:
            owner_team_mail = request.user.email
            team_or_user_name = request.user.username
            participant.user_id = request.user.id
        participant.save()

        domain = request.META['HTTP_HOST']
        url = '{}{}{}'.format('https://', domain, event.url)
        data = {
            "owner_name": event.get_owner().name,
            "event_name": event.name,
            "event_url": url,
            "owner_team_mail": owner_team_mail,
        }
        owner_event_send_thanks(data=data)

        # send email to org
        data.update({
            "team_or_user_name": team_or_user_name,
            "owner_team_mail": event.get_owner().user.email
        })

        # send email to team/user
        team_or_user_send_join_event(data=data)

        if event:
            return Response(data={"message": "Event join successfully", "event_url": event.url}, status=HTTP_200_OK)
        else:
            return Response(data={"Missing param event_id"}, status=HTTP_400_BAD_REQUEST)


class MediasEvent(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description='Lấy danh sách các ảnh của sự kiện',
        operation_summary='Lấy danh sách các ảnh của sự kiện',
        manual_parameters=[
            openapi.Parameter('event_id', type=openapi.TYPE_INTEGER, in_=openapi.IN_QUERY,
                              description='Id của sự kiện')
        ],
        responses={
            HTTP_200_OK: openapi.Response(
                description='', schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI))
            ),
            HTTP_404_NOT_FOUND: openapi.Response(
                description='', examples={
                    "status": "Event not found",
                }
            )
        }
    )
    def list_images(self, request):
        try:
            event = Event.objects.get(id=request.GET.get('event_id'))
            images = event.media_set.filter(set_as_cover=False)
            data = []
            for image in images:
                if image.image:
                    data.append(image.get_image_url())
            return Response(data=data, status=HTTP_200_OK)
        except (Event.DoesNotExist, Exception) as e:
            if len(e.args) == 2:
                msg, code = e.args
            else:
                msg, code = e.args, None
            return Response(data={'status': 'Failed!', 'message': f'{msg}'},
                            status=code if code is not None else HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description='Cập nhật medias của sự kiện',
        operation_summary='Cập nhật medias của sự kiện',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT, properties={
                'event_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID của event'),
                'images': openapi.Schema(type=openapi.TYPE_ARRAY, description='Array ảnh cần upload',
                                         items=openapi.Schema(type=openapi.TYPE_FILE)),
                'images_delete': openapi.Schema(type=openapi.TYPE_ARRAY, description='Array uid ảnh cần xóa',
                                                items=openapi.Schema(type=openapi.TYPE_STRING)),
            }
        ),
        responses={
            HTTP_200_OK: openapi.Response(
                description='', schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI))
            ),
            HTTP_404_NOT_FOUND: openapi.Response(
                description='', examples={
                    "status": "Event not found",
                }
            )
        }
    )
    def update_medias(self, request):
        try:
            event_id = request.data.get('event_id')
            images = request.FILES.getlist('images')
            images_delete = request.data.get('images_delete')
            event = Event.objects.get(id=event_id)
            # check permission
            if event.team and request.user.id not in event.team.userexperience_set.values_list('user_id', flat=True):
                raise Exception('Permission Denied', HTTP_403_FORBIDDEN)
            if event.organization and request.user.id not in event.organization.userexperience_set.values_list(
                    'user_id',
                    flat=True):
                raise Exception('Permission Denied', HTTP_403_FORBIDDEN)
            # add media into event
            if len(images) != 0:
                for image in images:
                    Media.objects.create(event=event, media_type='img', image=image)
            medias_of_event = event.media_set.filter(set_as_cover=False)
            if images_delete:
                for m_d in json.loads(images_delete):
                    medias_of_event.filter(image__icontains=m_d).delete()
                    cloudinary.api.delete_resources(m_d)
            data = []
            for media in medias_of_event:
                if media.image:
                    data.append(media.get_image_url())
            return Response(data={'status': 'Success', 'data': data}, status=HTTP_200_OK)
        except (Event.DoesNotExist, Exception) as e:
            if len(e.args) == 2:
                msg, code = e.args
            else:
                msg, code = e.args, None
            return Response(data={'status': 'Failed!', 'message': f'{msg}'},
                            status=code if code is not None else HTTP_404_NOT_FOUND)


# =====================================  FUNCTION BASE VIEWS ===================================


@swagger_auto_schema(
    method='POST',
    operation_description='Upload ảnh đại diện của sự kiện',
    operation_summary='Upload ảnh đại diện của sự kiện',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'currentOwnerId': openapi.Schema(type=openapi.TYPE_INTEGER, description='Id của event'),
            'avatar': openapi.Schema(type=openapi.TYPE_FILE, description='File ảnh', format=openapi.FORMAT_BINARY)
        }
    ),
    responses={
        HTTP_200_OK: openapi.Response(
            description='', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING, default='success'),
                    'avatar_url': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_SLUG),
                }
            )
        ),
        HTTP_400_BAD_REQUEST: openapi.Response(
            description='', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        default='avatar_img is empty'
                    ),
                }
            )
        )
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication, SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def event_upload_avatar(request):
    current_owner_id, avatar_img = data_from_method_post_put_delete(request, 'currentOwnerId', 'avatar')

    if isinstance(avatar_img, File) and avatar_img.size == 0:
        return Response(data={'status': 'avatar_img is empty'}, status=HTTP_400_BAD_REQUEST)

    event = Event.objects.get(id=current_owner_id)
    if event.picture is not None:
        cloudinary.api.delete_resources(event.picture.public_id)
    event.picture = avatar_img
    event.save()
    # save picture để tạo picture_url
    event.picture_url = event.picture.build_url(width=200, height=200,
                                                secure=True,
                                                crop='thumb') if event.picture is not None else None
    event.save()
    # save để lưu picture_url
    return Response(data={'status': 'success', 'avatar_url': event.picture_url}, status=HTTP_200_OK)


@swagger_auto_schema(
    method='POST',
    operation_description='Cập nhật ảnh bìa của sự kiện',
    operation_summary='Cập nhật ảnh bìa của sự kiện',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'currentOwnerId': openapi.Schema(type=openapi.TYPE_INTEGER, description='Id của event'),
            'cover': openapi.Schema(type=openapi.TYPE_FILE, description='File ảnh', format=openapi.FORMAT_BINARY)
        }
    ),
    responses={
        HTTP_200_OK: openapi.Response(
            description='', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING, default='success'),
                    'cover_url': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_SLUG),
                }
            )
        ),
        HTTP_400_BAD_REQUEST: openapi.Response(
            description='', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        enum=[
                            'Missing owner id or cover image',
                            'Cover is empty'
                        ]
                    ),
                }
            )
        )
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication, SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def event_upload_cover(request):
    current_owner_id = request.data.get('currentOwnerId')
    cover_img = request.data.get('cover')

    if isinstance(cover_img, File) and cover_img.size == 0:
        return Response(data={'status': 'Cover is empty'}, status=HTTP_400_BAD_REQUEST)

    if not all([current_owner_id, cover_img]):
        return Response(data={'status': "Missing param currentOwnerId or cover"}, status=HTTP_400_BAD_REQUEST)
    medias = Media.objects.filter(Q(event_id=current_owner_id) & Q(set_as_cover=True))
    return update_cover(medias, cover_img, current_owner_id, 'event', 200)


@swagger_auto_schema(
    method='POST',
    operation_description='Đăng ảnh và văn bản lên phần thảo luận trên trang sự kiện',
    operation_summary='Đăng ảnh và văn bản lên phần thảo luận trên trang sự kiện',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "currentOwnerId": openapi.Schema(description='id của event', type=openapi.TYPE_INTEGER),
            "text": openapi.Schema(type=openapi.TYPE_STRING),
            "images": openapi.Schema(description='Mảng file hình ảnh trong bài viết', type=openapi.TYPE_ARRAY,
                                     items=openapi.Schema(
                                         type=openapi.TYPE_FILE
                                     )),
            "privacy_id": openapi.Schema(type=openapi.TYPE_INTEGER),
        }
    ),
    responses={
        HTTP_201_CREATED: openapi.Response(
            description='', examples={
                "status": "uploaded",
                "data": {}
            }
        )
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication, SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def upload_a_post(request):
    current_owner_id = int(request.data.get('currentOwnerId'))
    text = request.data.get('text')
    images = request.data.getlist('images')
    privacy_id = request.data.get('privacy_id')
    # # Lưu bài viết
    post = Post.objects.create(user_id=request.user.id, event_id=int(current_owner_id),
                               privacy_setting_id=int(privacy_id),
                               content=text)
    # Lưu media được đính kèm với bài post
    if len(images) != 0:
        for image in images:
            Media.objects.create(post=post, media_type='img', image=image)
    return Response(data={'status': 'uploaded', 'data': PostSerializer(post, context={'request': request}).data},
                    status=HTTP_201_CREATED)


@swagger_auto_schema(
    method='DELETE',
    operation_description='Xóa một bài đăng trên trang sự kiện',
    operation_summary='Xóa một bài đăng trên trang sự kiện',
    manual_parameters=[openapi.Parameter('post_id', type=openapi.TYPE_INTEGER, in_=openapi.IN_PATH,
                                         description='ID của bài đăng')],
    responses={
        HTTP_201_CREATED: openapi.Response(
            description='', examples={
                "status": "Deleted",
            }
        )
    }
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication, SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_a_post(request, post_id=None):
    try:
        post = Post.objects.get(id=post_id)
        # Check permission delete post
        if post.user.id == request.user.id or post.event.get_owner().user.id == request.user.id:
            # Xóa các hình ảnh đính kèm trong bài viết
            for media in post.media_set.all():
                cloudinary.api.delete_resources(media.image.public_id) if media.image else None
                media.delete()
            post.delete()
        else:
            return Response(data={'message': 'Permission denied'}, status=HTTP_403_FORBIDDEN)
        return Response(data={'status': 'Deleted'}, status=HTTP_200_OK)
    except (Post.DoesNotExist, Exception) as e:
        if len(e.args) == 2:
            msg, code = e.args
        else:
            msg, code = e.args, None
        return Response(data={'status': 'Failed!', 'message': f'{msg}'},
                        status=code if code is not None else HTTP_404_NOT_FOUND)
