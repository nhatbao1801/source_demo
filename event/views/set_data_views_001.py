import json

import cloudinary.api
from django.core.mail import EmailMessage
from django.db.models import Q, Avg, F, Value, CharField, Sum
from django.db.models.functions import Concat
from django.http import HttpResponse
from django.template.loader import render_to_string
from drf_yasg import openapi
from drf_yasg.openapi import TYPE_OBJECT, Schema, TYPE_STRING, TYPE_INTEGER, FORMAT_URI, TYPE_ARRAY, TYPE_NUMBER, \
    FORMAT_SLUG, FORMAT_EMAIL, FORMAT_FLOAT, TYPE_FILE, TYPE_BOOLEAN, FORMAT_DOUBLE, FORMAT_DATETIME, Parameter, \
    IN_QUERY, FORMAT_DECIMAL
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND,
                                   HTTP_200_OK, HTTP_406_NOT_ACCEPTABLE, HTTP_403_FORBIDDEN,
                                   HTTP_401_UNAUTHORIZED)
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

# from hSpace import settings
# from hSchool.models import (Course, Benefit, CourseCategory, CourseInstructor, ReviewInstructor, JoinedCourse,
#                             CourseRating, ApplyTeaching, ModuleLesson, Translate, CourseSubCategory)
# from hSchool.schemas.course_category_schema import CourseCategorySchema
# from hSchool.schemas.course_subcategory_schema import CourseSubCategorySchema
# from hSchool.serializers import CourseSerializer, ReviewInstructorSerializer, CourseInstructorSerializer
# from hSchool.serializers.course_category_serializer import CourseCategorySerializer
# from hSchool.serializers.course_subcategory_serializer import CourseSubCategorySerializer
# from main.models import Area, User, Type, Invitation, Role, Media
# from main.serializers.area_serializer import AreaSerializer
# from main.serializers.type_serializer import TypeSerializer
# from startup.views.get_data_views import get_owner
from hSpace import settings
from models import *
from hSchool.schemas.course_category_schema import CourseCategorySchema
from hSchool.schemas.course_subcategory_schema import CourseSubCategorySchema
from hSchool.serializers import CourseSerializer, ReviewInstructorSerializer, CourseInstructorSerializer
from hSchool.serializers.course_category_serializer import CourseCategorySerializer
from hSchool.serializers.course_subcategory_serializer import CourseSubCategorySerializer
from main.models import Area, User, Type, Invitation, Role, Media
from main.serializers.area_serializer import AreaSerializer
from main.serializers.type_serializer import TypeSerializer
from startup.views.get_data_views import get_owner
from utils import data_from_method_post_put_delete, none_any, get_translate
from utils.h_paginator import h_paginator
from utils.send_notification import send_notification


class SchemaBase:
    metadata = Schema(
        type=TYPE_OBJECT,
        properties={
            "valid_page": Schema(type=TYPE_BOOLEAN),
            "count": Schema(type=TYPE_BOOLEAN),
            "num_pages": Schema(type=TYPE_BOOLEAN),
            "page_range": Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_INTEGER)),
            "has_next": Schema(type=TYPE_BOOLEAN),
            "has_previous": Schema(type=TYPE_BOOLEAN),
            "current_page": Schema(type=TYPE_INTEGER),
            "next_page_number": Schema(type=TYPE_INTEGER),
            "previous_page_number": Schema(type=TYPE_INTEGER)
        }
    )
    creator_schema = Schema(
        type=TYPE_OBJECT, properties={
            "id": Schema(type=TYPE_INTEGER),
            "username": Schema(type=TYPE_STRING),
            "first_name": Schema(type=TYPE_STRING),
            "last_name": Schema(type=TYPE_STRING),
            "email": Schema(type=TYPE_STRING, format=FORMAT_EMAIL),
            "phone_number": Schema(type=TYPE_STRING),
            "picture": Schema(type=TYPE_STRING, format=FORMAT_URI),
            "short_bio": Schema(type=TYPE_STRING),
            "url": Schema(type=TYPE_STRING, format=FORMAT_SLUG),
            "something_great_to_tell": Schema(type=TYPE_STRING),
            "profile_strength": Schema(type=TYPE_NUMBER, format=FORMAT_FLOAT),
            "types": Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_STRING, description='[]')),
            "external_link": Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_OBJECT, properties={
                "id": Schema(type=TYPE_INTEGER),
                "site_origin": Schema(type=TYPE_STRING),
                "url": Schema(type=TYPE_STRING, format=FORMAT_URI),
            })),
            "c_follower": Schema(type=TYPE_INTEGER),
            "c_following": Schema(type=TYPE_INTEGER),
        })
    rating_range = Schema(type=TYPE_OBJECT, properties={
        "sum": Schema(type=TYPE_NUMBER, format=FORMAT_FLOAT,
                      description='Tổng phần trăm lượng rating'),
        "1": Schema(type=TYPE_NUMBER, format=FORMAT_FLOAT,
                    description='Tổng % rating 1 *'),
        'c_1': Schema(type=TYPE_INTEGER, description='Tổng số người rating 1 *'),
        "2": Schema(type=TYPE_NUMBER, format=FORMAT_FLOAT,
                    description='Tổng % rating 2 *'),
        'c_2': Schema(type=TYPE_INTEGER, description='Tổng số người rating 2 *'),
        "3": Schema(type=TYPE_NUMBER, format=FORMAT_FLOAT,
                    description='Tổng % rating 3 *'),
        'c_3': Schema(type=TYPE_INTEGER, description='Tổng số người rating 3 *'),
        "4": Schema(type=TYPE_NUMBER, format=FORMAT_FLOAT,
                    description='Tổng % rating 4 *'),
        'c_4': Schema(type=TYPE_INTEGER, description='Tổng số người rating 4 *'),
        "5": Schema(type=TYPE_NUMBER, format=FORMAT_FLOAT,
                    description='Tổng % rating 5 *'),
        'c_5': Schema(type=TYPE_INTEGER, description='Tổng số người rating 5 *'),
    })
    reviews = Schema(type=TYPE_OBJECT, properties={
        "data": Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_OBJECT, properties={
            "id": Schema(type=TYPE_INTEGER),
            "username": Schema(type=TYPE_STRING),
            "slug": Schema(type=TYPE_STRING, format=FORMAT_SLUG),
            "comment": Schema(type=TYPE_STRING),
            "num_star": Schema(type=TYPE_INTEGER),
            "picture": Schema(type=TYPE_STRING, format=FORMAT_URI),
            "comment_date": Schema(type=TYPE_STRING, format=FORMAT_DATETIME),
        })),
        "metadata_reviews": metadata
    })


class CreateCourseAPI(APIView, SchemaBase):
    authentication_classes = [JWTAuthentication, SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description='Thêm một khóa học',
        operation_summary='Thêm một khóa học',
        request_body=Schema(
            type=TYPE_OBJECT,
            properties={
                "course_category_id": Schema(type=TYPE_INTEGER),
                "category_name": Schema(type=TYPE_STRING, description='Có thể không dùng'),
                "sub_category_id": Schema(type=TYPE_INTEGER, description=''),
                "thumb": Schema(type=TYPE_FILE),
                "background": Schema(type=TYPE_FILE),
                "skills_accquired": Schema(type=TYPE_STRING, description='[1,2,3,4]'),
                "video_url_introduce ": Schema(type=TYPE_STRING, description='', format=FORMAT_SLUG),
                "instructors": Schema(type=TYPE_STRING, description='[1,2,3,4]'),
                "price": Schema(type=TYPE_INTEGER, format=FORMAT_DECIMAL, description='99.99'),
                "level": Schema(type=TYPE_STRING, description='Level của khóa học',
                                enum=['Beginer', 'Intermediate', 'Advance']),
                "online_hours": Schema(type=TYPE_INTEGER, description='10'),
                "about_vi": Schema(type=TYPE_STRING, description='about'),
                "about_en": Schema(type=TYPE_STRING, description='about'),
                "career_orientation_vi": Schema(type=TYPE_STRING, description='description'),
                "career_orientation_en": Schema(type=TYPE_STRING, description='description'),
                "title_vi": Schema(type=TYPE_STRING, description='title_vi'),
                "title_en": Schema(type=TYPE_STRING, description='title_en'),
                "course_for": Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_OBJECT, properties={
                    'id': Schema(type=TYPE_INTEGER, description='Id của đối tượng học/ Null hoặc một id đã có'),
                    'name': Schema(type=TYPE_STRING, description='Tên của đối tượng học')
                })),
                "benefits": Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_OBJECT, properties={
                    'id': Schema(type=TYPE_INTEGER, description='Id của benefit/ Null hoặc một id đã có'),
                    'content': Schema(type=TYPE_STRING, description='Content của benefit')
                })),
            }
        ),
        responses={
            HTTP_201_CREATED: openapi.Response(
                description='Thêm thành công',
                schema=Schema(
                    type=TYPE_OBJECT,
                    properties={
                        "status": Schema(type=TYPE_STRING),
                        "new_course": Schema(type=TYPE_OBJECT, properties={
                            "id": Schema(type=TYPE_INTEGER),
                            "picture": Schema(type=TYPE_STRING, format=FORMAT_URI),
                            "price": Schema(type=TYPE_STRING, format=FORMAT_DECIMAL),
                            "title_vi": Schema(type=TYPE_STRING),
                            "title_en": Schema(type=TYPE_STRING),
                            "slug": Schema(type=TYPE_STRING, format=FORMAT_SLUG),
                            "about_vi": Schema(type=TYPE_STRING),
                            "about_en": Schema(type=TYPE_STRING),
                            "state": Schema(type=TYPE_STRING),
                            "career_orientation_vi": Schema(type=TYPE_STRING),
                            "career_orientation_en": Schema(type=TYPE_STRING),
                            "level": Schema(type=TYPE_STRING),
                            "skill_acquired": Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_OBJECT, properties={
                                "id": Schema(type=TYPE_INTEGER),
                                "name": Schema(type=TYPE_STRING),
                            })),
                            "instructors": Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_OBJECT, properties={
                                "id": Schema(type=TYPE_INTEGER),
                                "username": Schema(type=TYPE_STRING),
                                "url": Schema(type=TYPE_STRING, format=FORMAT_SLUG),
                                "picture": Schema(type=TYPE_STRING, format=FORMAT_URI),
                            })),
                            "creator": SchemaBase.creator_schema,
                            "course_for": Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_OBJECT, properties={
                                "id": Schema(type=TYPE_INTEGER),
                                "name": Schema(type=TYPE_STRING)
                            })),
                            "benefit": Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_OBJECT, properties={
                                "id": Schema(type=TYPE_INTEGER),
                                "content": Schema(type=TYPE_STRING)
                            })),
                            "background": Schema(type=TYPE_STRING, format=FORMAT_URI)
                        }),
                    }
                )
            ),
            HTTP_400_BAD_REQUEST: openapi.Response(
                description='Bad request',
                schema=Schema(
                    type=TYPE_OBJECT, properties={
                        "message": Schema(type=TYPE_STRING),
                    }
                )
            ),
            HTTP_404_NOT_FOUND: openapi.Response(
                description='Lỗi không tìm thấy',
                schema=Schema(
                    type=TYPE_OBJECT, properties={
                        "message": Schema(type=TYPE_STRING),
                    }
                )
            ),
            HTTP_401_UNAUTHORIZED: openapi.Response(
                description='Lỗi trả về',
                examples={
                    'status': 'failed',
                    'message': 'Kiểm tra lại email đăng nhập hoặc mặt khẩu'
                }
            )
        }

    )
    def post(self, request, *args, **kwargs):
        course_category_id, sub_category_id, skills_accquired, instructors, thumb, level, online_hours, about_vi, about_en, \
        career_orientation_vi, career_orientation_en, title_vi, title_en, course_for, benefits, video_url_introduce, price, background = data_from_method_post_put_delete(
            request,
            'course_category_id', 'sub_category_id', 'skills_accquired', 'instructors', 'thumb', 'level',
            'online_hours', 'about_vi', 'about_en', 'career_orientation_vi', 'career_orientation_en', 'title_vi',
            'title_en', 'course_for', 'benefits',
            'video_url_introduce', 'price', 'background'
        )
        # try:
        #     # Get category from Course category
        #     category = CourseCategory.objects.get(id=sub_category_id)
        # except CourseCategory.DoesNotExist:
        #     return Response(
        #         data={'status': 'Failed!', 'message': 'Missing sub_category_id or sub category does not exist'},
        #         status=HTTP_400_BAD_REQUEST)
        if skills_accquired is None or benefits is None:
            return Response(data={'status': 'Failed', 'message': 'Missing skills_accquired or benefits'},
                            status=HTTP_400_BAD_REQUEST)
        if title_vi is None or level is None:
            return Response(data={'status': 'Failed', 'message': 'Missing title or level'})

        new_course = Course()
        new_course.course_category_id_id = course_category_id
        new_course.course_subcategory_id = sub_category_id
        new_course.thumb = thumb
        new_course.level = level
        new_course.online_hours = online_hours
        new_course.about = about_vi
        new_course.career_orientation = career_orientation_vi
        new_course.title = title_vi
        new_course.price = price
        new_course.video_url_introduce = video_url_introduce
        new_course.creator_id = request.user.id
        new_course.save()

        trans = []
        if title_vi:
            trans.append(Translate(field='title', text=title_vi, language_id=1, course_id=new_course.id))
        if title_en:
            trans.append(Translate(field='title', text=title_en, language_id=2, course_id=new_course.id))

        if about_vi:
            trans.append(Translate(course=new_course, field='about', language_id=1, text=about_vi))
        if about_en:
            trans.append(Translate(course=new_course, field='about', language_id=2, text=about_vi))

        if career_orientation_vi:
            trans.append(Translate(course=new_course, field='career_orientation', language_id=1, text=career_orientation_vi))
        if career_orientation_en:
            trans.append(Translate(course=new_course, field='career_orientation', language_id=2, text=career_orientation_en))
        Translate.objects.bulk_create(trans)

        if background:
            Media.objects.create(set_as_cover=True, course_id=new_course.id, image=background)

        for skill_id in json.loads(skills_accquired):
            new_course.skills_accquired.add(Area.objects.get(id=skill_id))

        if course_for:
            for role in json.loads(course_for):
                _r = None
                if role['id']:
                    _r = Role.objects.get(pk=role['id'])
                else:
                    check_name = Role.objects.filter(name__exact=role['name'])
                    if check_name:
                        _r = check_name.first()
                    else:
                        _r = Role.objects.create(name=role['name'])

                new_course.course_for.add(_r)

        # for instructor_id in json.loads(instructors):
        # ci = [CourseInstructor(course_id=new_course.id, user=User.objects.get(id=instructor_id), rating=0, fee=0)
        #       for instructor_id in json.loads(instructors)]
        # CourseInstructor.objects.bulk_create(ci)

        # Add invite teaching
        subject = 'Invitation for teaching'
        title = 'Invitation for teaching'
        team_name = ''
        text = ''
        if instructors:
            for instructor_id in json.loads(instructors):
                _user = User.objects.get(id=instructor_id)
                Invitation.objects.create(
                    course=new_course,
                    to_user=_user,
                    init_message='Mời làm giảng viên',
                    is_accepted=False
                )
                mail_context = {
                    'title': title,
                    'text': text,
                    'username': _user.username,
                    'team_name': team_name,
                    'init_message': 'Mời làm giảng viên',
                    'profile_link': 'https://hspaces.net/hschool/courses/detail/' + str(
                        new_course.slug) + f'?viewAsId={instructor_id}',
                }
                body = render_to_string('startup/email/invitation_to_join_team.html', mail_context)
                reply_to = settings.DEFAULT_FROM_EMAIL

                user_sys_email = _user.email
                join_team_invitation_mail = EmailMessage(subject=subject, body=body,
                                                         to=[user_sys_email], reply_to=[reply_to])
                join_team_invitation_mail.content_subtype = 'html'
                join_team_invitation_mail.send(fail_silently=True)

            # ApplyTeaching.objects.create(is_accepted=False, course_id=new_course.id, user_id=_user.id)

        for benefit in json.loads(benefits):
            if benefit['id']:
                benefit_id = benefit['id']
            else:
                _be = Benefit.objects.create(content=benefit['content'])
                benefit_id = _be.id
            new_course.benefits.add(Benefit.objects.get(id=benefit_id))

        thumb = new_course.thumb.build_url(secure=True, transformation=[
            {'width': 237, 'height': 178, 'crop': 'thumb'}]) if new_course.thumb is not None else None

        _new_course = get_course_info(course=new_course, thumb=thumb, request=request)

        return Response(data={'status': 'success', 'new_course': _new_course},
                        content_type='application/json; charset=utf-8', status=HTTP_201_CREATED)


def get_skill_accquired(course):
    skills = [{"id": c.id, "name": c.name} for c in course.skills_accquired.all()]
    return skills


class UpdateCourse(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description='Cập nhập một khóa học',
        operation_summary='Cập nhập một khóa học',
        request_body=Schema(
            type=TYPE_OBJECT,
            properties={
                "course_category_id": Schema(type=TYPE_INTEGER, description='Không dùng nữa'),
                "category_name": Schema(type=TYPE_STRING, description=''),
                "sub_category_id": Schema(type=TYPE_INTEGER, description=''),
                "thumb": Schema(type=TYPE_FILE),
                "skills_accquired": Schema(type=TYPE_STRING, description='[1,2,3,4]'),
                "instructors": Schema(type=TYPE_STRING, description='[1,2,3,4]'),
                "video_url_introduce ": Schema(type=TYPE_STRING, description='', format=FORMAT_SLUG),
                # "benefits": Schema(type=TYPE_STRING, description='[1,2,3,4]'),
                "level": Schema(type=TYPE_INTEGER, description='1'),
                "online_hours": Schema(type=TYPE_INTEGER, description='10'),
                "about_vi": Schema(type=TYPE_STRING, description='abc def'),
                "about_en": Schema(type=TYPE_STRING, description='abc def'),
                "career_orientation_vi": Schema(type=TYPE_STRING, description='abc def'),
                "career_orientation_en": Schema(type=TYPE_STRING, description='abc def'),
                "title_vi": Schema(type=TYPE_STRING, description='abc def'),
                "title_en": Schema(type=TYPE_STRING, description='abc def'),
                "course_for": Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_OBJECT, properties={
                    'id': Schema(type=TYPE_INTEGER, description='Id của đối tượng học/ Null hoặc một id đã có'),
                    'name': Schema(type=TYPE_STRING, description='Tên của đối tượng học')
                })),
                "benefits": Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_OBJECT, properties={
                    'id': Schema(type=TYPE_INTEGER, description='Id benefit/ Null hoặc một id đã có'),
                    'content': Schema(type=TYPE_STRING, description='Tên của benefit')
                })),
            }
        ),
        responses={
            HTTP_200_OK: openapi.Response(
                description='Cập nhập thành công',
                schema=Schema(
                    type=TYPE_OBJECT,
                    properties={
                        "id": Schema(type=TYPE_INTEGER),
                        "picture": Schema(type=TYPE_STRING, format=FORMAT_URI),
                        "title_vip": Schema(type=TYPE_STRING),
                        "title_en": Schema(type=TYPE_STRING),
                        "slug": Schema(type=TYPE_STRING, format=FORMAT_SLUG),
                        "about": Schema(type=TYPE_STRING),
                        "state": Schema(type=TYPE_STRING),
                        "date_created": Schema(type=TYPE_STRING, format=FORMAT_DATETIME),
                        "career_orientation": Schema(type=TYPE_STRING),
                        "level": Schema(type=TYPE_STRING),
                        "is_rating": Schema(type=TYPE_BOOLEAN,
                                            description='User đang đăng nhập đã rating khóa học này chưa?'),
                        'isEnroll': Schema(type=TYPE_BOOLEAN,
                                           description='User đang đăng nhập có enroll course này chưa'),
                        'member': Schema(type=TYPE_INTEGER, description='Số lượng member'),
                        'rating': Schema(type=TYPE_STRING, format=FORMAT_FLOAT,
                                         description='Tổng số start rating khóa học'),
                        'c_rating': Schema(type=TYPE_INTEGER, description='Số lượng rating'),
                        'time': Schema(type=TYPE_STRING, description='Số lượng thời gian học'),
                        'category': Schema(type=TYPE_STRING),
                        'sub_category_name': Schema(type=TYPE_STRING),
                        'sub_category_id': Schema(type=TYPE_INTEGER),
                        "rating_range": SchemaBase.rating_range,
                        "skills_acquired": Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_OBJECT, properties={
                            "id": Schema(type=TYPE_INTEGER),
                            "name": Schema(type=TYPE_STRING),
                        })),
                        "instructors": Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_OBJECT, properties={
                            "id": Schema(type=TYPE_INTEGER),
                            "url": Schema(type=TYPE_STRING, format=FORMAT_SLUG),
                            "username": Schema(type=TYPE_STRING),
                            "first_name": Schema(type=TYPE_STRING),
                            "last_name": Schema(type=TYPE_STRING),
                            "email": Schema(type=TYPE_STRING),
                            "short_bio": Schema(type=TYPE_STRING),
                            "skills": Schema(type=TYPE_ARRAY,
                                             items=Schema(type=TYPE_OBJECT, properties={
                                                 "id": Schema(type=TYPE_INTEGER),
                                                 "name": Schema(type=TYPE_STRING),
                                             })),
                            "external_link": Schema(
                                type=TYPE_ARRAY,
                                items=Schema(type=TYPE_OBJECT, properties={
                                    "site_origin": Schema(type=TYPE_STRING, format=FORMAT_URI),
                                    "url": Schema(type=TYPE_STRING, format=FORMAT_SLUG),
                                })
                            ),
                            "is_rating": Schema(type=TYPE_BOOLEAN,
                                                description='User đang đăng nhập đã rating instructor này chưa?'),
                            "rating": Schema(type=TYPE_NUMBER, format=FORMAT_FLOAT),
                            "c_rating": Schema(type=TYPE_INTEGER),
                            "c_course": Schema(type=TYPE_INTEGER),
                            "price": Schema(type=TYPE_NUMBER, format=FORMAT_DOUBLE),
                            "avatar": Schema(type=TYPE_STRING, format=FORMAT_URI),
                            "c_follower": Schema(type=TYPE_INTEGER),
                            "c_following": Schema(type=TYPE_INTEGER),
                        })),
                        "creator": SchemaBase.creator_schema,
                        "course_for": Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_OBJECT, properties={
                            "id": Schema(type=TYPE_INTEGER),
                            "name": Schema(type=TYPE_STRING)
                        })),
                        "benefit": Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_OBJECT, properties={
                            "id": Schema(type=TYPE_INTEGER),
                            "content": Schema(type=TYPE_STRING)
                        }))
                    }
                )
            ),
            HTTP_400_BAD_REQUEST: openapi.Response(
                description='Bad request',
                schema=Schema(
                    type=TYPE_OBJECT, properties={
                        "message": Schema(type=TYPE_STRING),
                    }
                )
            ),
            HTTP_404_NOT_FOUND: openapi.Response(
                description='Lỗi không tìm thấy',
                schema=Schema(
                    type=TYPE_OBJECT, properties={
                        "message": Schema(type=TYPE_STRING),
                    }
                )
            ),
            HTTP_401_UNAUTHORIZED: openapi.Response(
                description='Lỗi trả về',
                examples={
                    'status': 'failed',
                    'message': 'Kiểm tra lại email đăng nhập hoặc mặt khẩu'
                }
            )
        }

    )
    def put(self, request, pk=None):
        sub_category_id, category_name, skills_accquired, instructors, thumb, level, online_hours, about, \
        career_orientation_vi, career_orientation_en, title_vi, title_en, about_vi, about_en, benefits, course_for, video_url_introduce, price, background = data_from_method_post_put_delete(
            request,
            'sub_category_id', 'category_name', 'skills_accquired', 'instructors', 'thumb', 'level',
            'online_hours', 'about', 'career_orientation_vi', 'career_orientation_en', 'title_vi', 'title_en',
            'about_vi', 'about_en', 'benefits', 'course_for', 'video_url_introduce', 'price', 'background'
        )
        try:
            # Get the course from db
            course = Course.objects.get(pk=pk)
            if request.user.id != course.creator_id:
                raise Exception('Do not have permission', 403)
            course_serializer = CourseSerializer(data={
                'course_category_id': sub_category_id, 'skills_accquired': skills_accquired,
                'instructors': instructors, 'thumb': thumb, 'level': level,
                'online_hours': online_hours,
                'benefits': benefits, 'video_url_introduce': video_url_introduce, 'price': price,
                'background': background
            }, partial=True)
            if course_serializer.is_valid():
                course.course_category_id_id = sub_category_id
                # Delete course thumb
                if course.thumb is not None and thumb is not None:
                    cloudinary.api.delete_resources(course.thumb.public_id)
                    course.thumb = course_serializer.validated_data.get('thumb')
                if course.media_set.filter(course=course).first() is not None and background is not None:
                    m = course.media_set.filter(course=course).first()
                    if m:
                        cloudinary.api.delete_resources(m.image.public_id)
                        m.delete()
                    Media.objects.create(course_id=course.id, set_as_cover=True,
                                         image=background)
                elif course.media_set.filter(course=course).first() is None and background is not None:
                    Media.objects.create(course_id=course.id, set_as_cover=True,
                                         image=background)
                if course_serializer.validated_data.get('level'):
                    course.level = course_serializer.validated_data.get('level')
                if course_serializer.validated_data.get('online_hours'):
                    course.online_hours = course_serializer.validated_data.get('online_hours')
                if video_url_introduce:
                    course.video_url_introduce = video_url_introduce
                if price:
                    course.price = price
                course.save()

                if title_vi:
                    course.title = title_vi
                    t_t = Translate.objects.filter(course=course, field='title', language_id=1)
                    if t_t:
                        Translate.objects.filter(course=course, field='title', language_id=1).update(text=title_vi)
                    else:
                        Translate.objects.create(course=course, field='title', language_id=1, text=title_vi)
                if title_en:
                    t_t = Translate.objects.filter(course=course, field='title', language_id=2)
                    if t_t:
                        Translate.objects.filter(course=course, field='title', language_id=2).update(text=title_en)
                    else:
                        Translate.objects.create(course=course, field='title', language_id=2, text=title_en)

                if about_vi:
                    course.about = about_vi
                    t_a = Translate.objects.filter(course=course, field='about', language_id=1)
                    if t_a:
                        Translate.objects.filter(course=course, field='about', language_id=1).update(text=about_vi)
                    else:
                        Translate.objects.create(course=course, field='about', language_id=1, text=about_vi)
                if about_en:
                    t_a = Translate.objects.filter(course=course, field='about', language_id=2)
                    if t_a:
                        Translate.objects.filter(course=course, field='about', language_id=2).update(text=about_en)
                    else:
                        Translate.objects.create(course=course, field='about', language_id=2, text=about_en)

                if career_orientation_vi:
                    course.career_orientation = career_orientation_vi
                    t_co = Translate.objects.filter(course=course, field='career_orientation', language_id=1)
                    if t_co:
                        Translate.objects.filter(course=course, field='career_orientation', language_id=1).update(
                            text=career_orientation_vi)
                    else:
                        Translate.objects.create(course=course, field='career_orientation', language_id=1,
                                                 text=career_orientation_vi)

                if career_orientation_en:
                    t_co = Translate.objects.filter(course=course, field='career_orientation', language_id=2)
                    if t_co:
                        Translate.objects.filter(course=course, field='career_orientation', language_id=2).update(
                            text=career_orientation_en)
                    else:
                        Translate.objects.create(course=course, field='career_orientation', language_id=2,
                                                 text=career_orientation_en)

                if skills_accquired:
                    course.skills_accquired.clear()
                    for skill_id in json.loads(skills_accquired):
                        course.skills_accquired.add(Area.objects.get(id=skill_id))

                if course_for:
                    for role in json.loads(course_for):
                        _r = None
                        if role['id']:
                            _r = Role.objects.get(pk=role['id'])
                        else:
                            check_name = Role.objects.filter(name__exact=role['name'])
                            if check_name:
                                _r = check_name.first()
                            else:
                                _r = Role.objects.create(name=role['name'])

                        course.course_for.add(_r)

                subject = 'Invitation for teaching'
                title = 'Invitation for teaching'
                team_name = ''
                text = ''
                if instructors:
                    # Add invite teaching

                    for instructor_id in json.loads(instructors):
                        _user = User.objects.get(id=instructor_id)
                        Invitation.objects.create(
                            course=course,
                            to_user=_user,
                            init_message='Mời làm giảng viên',
                            is_accepted=False
                        )
                        mail_context = {
                            'title': title,
                            'text': text,
                            'username': _user.username,
                            'team_name': team_name,
                            'init_message': 'Mời làm giảng viên',
                            'profile_link': 'https://hspaces.net/hschool/courses/detail/' + str(
                                course.slug) + f'?viewAsId={instructor_id}',
                        }
                        body = render_to_string('startup/email/invitation_to_join_team.html', mail_context)
                        reply_to = settings.DEFAULT_FROM_EMAIL

                        user_sys_email = _user.email
                        join_team_invitation_mail = EmailMessage(subject=subject, body=body,
                                                                 to=[user_sys_email], reply_to=[reply_to])
                        join_team_invitation_mail.content_subtype = 'html'
                        join_team_invitation_mail.send(fail_silently=True)

                        # ApplyTeaching.objects.create(is_accepted=False, course_id=course.id, user_id=_user.id)

                if benefits:
                    course.benefits.clear()
                    for benefit in json.loads(benefits):
                        if benefit['id']:
                            benefit_id = benefit['id']
                        else:
                            _be = Benefit.objects.create(content=benefit['content'])
                            benefit_id = _be.id
                        course.benefits.add(Benefit.objects.get(id=benefit_id))

                # Build url for course thumb
                thumb = course.thumb.build_url(width=237, height=178, secure=True,
                                               crop='thumb') if course.thumb is not None else None
                content = get_course_info(course=course, thumb=thumb, request=request)

                return Response(data=content, status=HTTP_200_OK)
            else:
                return Response(data=course_serializer.errors, status=HTTP_400_BAD_REQUEST)
        except (Course.DoesNotExist, Exception) as e:
            if len(e.args) == 2:
                msg, code = e.args
            else:
                msg, code = e.args, None
            return Response(data={'status': f'{msg}'}, status=code if code is not None else HTTP_404_NOT_FOUND)


def get_course_info(course=None, thumb=None, request=None, compact=None):
    if not course:
        return {}
    rt = course.courserating_set.aggregate(Avg('num_star'))
    from hSchool.views.get_data_views import get_skill_required
    from hSchool.views.get_data_views import get_rating
    from hSchool.views.get_data_views import get_course_module
    from hSchool.views.get_data_views import get_members_join
    from hSchool.views.get_data_views import get_reviews
    from hSchool.views.get_data_views import get_faqs
    from hSchool.views.get_data_views import get_instructors
    from hSchool.views.get_data_views import get_course_for
    from hSchool.views.get_data_views import get_benefit
    from hSchool.views.get_data_views import get_program_experience
    from hSchool.views.get_data_views import get_background

    _course_category = None
    if course.course_category_id and course.course_category_id:
        _course_category = course.course_category_id.name

    course_trans = course.translate_set.all()
    title_vi = get_translate(_objects=course_trans, _field='title',
                             _language_id=1) if course_trans.count() > 0 else course.title
    title_en = get_translate(_objects=course_trans, _field='title', _language_id=2)

    if compact:
        return {
            'id': course.id,
            'picture': thumb,
            'title': course.title,
            'title_vi': title_vi,
            'title_en': title_en,
            'slug': course.slug,
            'c_rating': course.courserating_set.count(),
            'c_member': course.joinedcourse_set.count(),
        }

    ml = ModuleLesson.objects.filter(course_module__course=course)
    c_lesson = ml.count()
    c_lesson_complete = ml.filter(
        Q(modulelessonviewed__user_id=request.user.id) & Q(modulelessonviewed__views_time__gt=0)).count()
    c_duration = ml.aggregate(c_duration=Sum('duration'))
    current_lesson = ml.filter(
        Q(modulelessonviewed__user_id=request.user.id) & Q(modulelessonviewed__current_view=True)
    ).first()
    first_lesson = ml.order_by('id').first()

    current_lesson_id = None
    if current_lesson_id:
        current_lesson_id = current_lesson.id
    elif first_lesson:
        current_lesson_id = first_lesson.id

    about_vi = get_translate(_objects=course_trans, _field='about',
                             _language_id=1) if course_trans.count() > 0 else course.about
    about_en = get_translate(_objects=course_trans, _field='about', _language_id=2)

    career_orientation_vi = get_translate(_objects=course_trans, _field='career_orientation',
                                          _language_id=1) if course_trans.count() > 0 else course.career_orientation
    career_orientation_en = get_translate(_objects=course_trans, _field='career_orientation', _language_id=2)

    background = get_background(course=course)

    course_info = {
        'id': course.id,
        'isEnroll': True if request.user.id in course.joinedcourse_set.values_list('user_id', flat=True) else False,
        'is_rating': True if request.user.id in course.courserating_set.values_list('user_id', flat=True) else False,
        'is_favorite': True if request.user in course.users_favorite.all() else False,
        'picture': thumb,
        'background': background,
        'slug': course.slug,
        'title': course.title,
        'title_vi': title_vi,
        'title_en': title_en,
        'video_url_introduce': course.video_url_introduce,
        'c_member': course.joinedcourse_set.count(),
        'rating': round(rt['num_star__avg'], 1) if rt['num_star__avg'] else 0,
        'price': course.price_display,
        'c_rating': course.courserating_set.count(),
        'c_lesson': c_lesson,
        'c_lesson_complete': c_lesson_complete,
        'c_hours': c_duration['c_duration'] / 60 if c_duration['c_duration'] and c_duration['c_duration'] > 0 else 0,
        'current_lesson_id': current_lesson_id,
        'time': course.online_hours,
        'about': course.about,
        'about_vi': about_vi,
        'about_en': about_en,
        'state': course.state,
        'date_created': course.date_created.strftime('%H:%M %d/%m/%Y') if course.date_created else None,
        'category': _course_category,
        'category_name': course.course_category_id.name if course.course_category_id else None,
        'category_id': course.course_category_id.id if course.course_category_id else None,
        'sub_category_name': course.course_subcategory.name if course.course_subcategory else None,
        'sub_category_id': course.course_subcategory.id if course.course_subcategory else None,
        'skills_acquired': get_skill_required(course),
        "instructors": get_instructors(course=course, request=request),
        'level': course.level,
        'career_orientation': course.career_orientation,
        'career_orientation_vi': career_orientation_vi,
        'career_orientation_en': career_orientation_en,
        "rating_range": get_rating(course),
        "creator": get_owner(course=course),
        "skill_acquired": get_skill_required(course),
        "benefit": get_benefit(course=course),
        "modules": get_course_module(course),
        "members": get_members_join(course),
        "reviews": get_reviews(course=course, request=request),
        "faqs": get_faqs(course),
        "course_for": get_course_for(course=course),
        "program_experience": get_program_experience(course=course)

    }

    return course_info


class DeleteCourse(APIView):

    @swagger_auto_schema(
        operation_description='Xóa một khóa học',
        operation_summary='Xóa  một khóa học',
        responses={
            HTTP_200_OK: openapi.Response(
                description='Xóa thành công',
                schema=Schema(
                    type=TYPE_OBJECT,
                    properties={
                        "message": Schema(type=TYPE_STRING)
                    }
                )
            ),
            HTTP_404_NOT_FOUND: openapi.Response(
                description='Lỗi không tìm thấy',
                schema=Schema(
                    type=TYPE_OBJECT, properties={
                        "message": Schema(type=TYPE_STRING),
                    }
                )
            ),
            HTTP_401_UNAUTHORIZED: openapi.Response(
                description='Lỗi trả về',
                examples={
                    'status': 'failed',
                    'message': 'Kiểm tra lại email đăng nhập hoặc mặt khẩu'
                }
            )
        }

    )
    def delete(self, request, pk=None):
        try:
            course = Course.objects.get(pk=pk)
            if request.user.id != course.creator_id:
                raise Exception('Do not have permission', 403)
            course.delete()
            return Response(data={'status': 'Deleted!'}, status=HTTP_200_OK)
        except (Course.DoesNotExist, Exception) as e:
            if len(e.args) == 2:
                msg, code = e.args
            else:
                msg, code = e.args, None
            return Response(data={'status': f'{msg}'}, status=code if code is not None else HTTP_404_NOT_FOUND)


class DeleteMultipleCourse(APIView):
    @swagger_auto_schema(
        operation_description='Xóa nhiều khóa học',
        operation_summary='Xóa nhiều khóa học',
        manual_parameters=[
            openapi.Parameter('course_id', openapi.IN_QUERY, description='[1,2,3,4]', type=openapi.TYPE_STRING)
        ],
        responses={
            HTTP_200_OK: openapi.Response(
                description='',
                examples={
                    'status': 'Deleted!',
                    'deleted_course_ids': '[1,2,3]'
                }
            ),
            HTTP_400_BAD_REQUEST: openapi.Response(
                description='', examples={
                    'status': ['Missing param course_id',
                               'Wrong data format course_id must be a list']
                }
            ),
            HTTP_403_FORBIDDEN: openapi.Response(
                description='', examples={
                    'status': 'Do not have permission [13,25,3,4]'
                }
            ),
            HTTP_404_NOT_FOUND: openapi.Response(
                description='', examples={
                    'status': '... does not exist'
                }
            )
        }
    )
    def delete(self, request):
        try:
            course_id, = data_from_method_post_put_delete(request, 'course_id')
            if course_id is None or course_id == '':
                return Response(data={'status': 'Missing param course_id'}, status=HTTP_400_BAD_REQUEST)
            course_ids = json.loads(course_id)
            deleted_course_ids, not_deleted_ids = [], []
            if isinstance(course_ids, list):
                for pk in course_ids:
                    course = Course.objects.get(pk=pk)
                    if request.user.id != course.creator_id:
                        not_deleted_ids.append(pk)
                        continue
                    course.delete()
                    deleted_course_ids.append(pk)
            else:
                return Response(data={'status': 'Wrong data format course_id must be a list'},
                                status=HTTP_400_BAD_REQUEST)
            if len(not_deleted_ids) != 0:
                raise Exception(f'Do not have permission {not_deleted_ids}', 403)
            return Response(data={'status': 'Deleted!', 'deleted_course_ids': deleted_course_ids},
                            status=HTTP_200_OK)
        except (Course.DoesNotExist, Exception) as e:
            if len(e.args) == 2:
                msg, code = e.args
            else:
                msg, code = e.args, None
            return Response(data={'status': f'{msg}'}, status=code if code is not None else HTTP_404_NOT_FOUND)


class ReviewInstructorViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description='Danh sách các instructor kèm thông tin của một khóa học',
        operation_summary='Danh sách các instructor kèm thông tin của một khóa học',
        manual_parameters=[
            openapi.Parameter('course_id', openapi.IN_QUERY, description='', required=True, type=openapi.TYPE_INTEGER)
        ],
        responses={
            HTTP_200_OK: openapi.Response(
                description='',
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'course_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'instructor_info': openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'username': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'url': openapi.Schema(type=openapi.TYPE_STRING),
                                    'picture': openapi.Schema(type=openapi.TYPE_STRING)
                                }
                            ),
                            'rating': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'fee': openapi.Schema(type=openapi.TYPE_INTEGER)
                        }
                    )
                )
            )
        }
    )
    def list(self, request):
        course_id = request.query_params.get('course_id')
        if not course_id or course_id == '':
            return Response(data={'status': 'Missing params course_id or course_id '},
                            status=HTTP_400_BAD_REQUEST)
        try:
            # Get all data in hschool_course_instructors with give course_id
            course_instructors = Course.objects.get(pk=course_id).courseinstructor_set.all()
            # Return information about instructor
            course_instructors_serializers = CourseInstructorSerializer(instance=course_instructors,
                                                                        many=True)
            return Response(data=course_instructors_serializers.data, status=HTTP_200_OK)
        except (User.DoesNotExist, Exception) as e:
            if len(e.args) == 2:
                msg, code = e.args
            else:
                msg, code = e.args, None
            return Response(data={'status': f'{msg}'}, status=code if code is not None else HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description='Tạo một review cho một instructor',
        operation_summary='Tạo một review cho một instructor',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'content': openapi.Schema(description='Nội dung review', type=openapi.TYPE_STRING),
                'rating': openapi.Schema(description='Rating giảng viên', type=openapi.TYPE_NUMBER),
                'instructor': openapi.Schema(description='Id giảng viên cần đánh giá', type=openapi.TYPE_NUMBER),
                'course': openapi.Schema(description='Id của khóa học', type=openapi.TYPE_NUMBER),
                'reviewer': openapi.Schema(description='Id người đánh giá', type=openapi.TYPE_NUMBER),
            }
        ),
        responses={
            HTTP_201_CREATED: openapi.Response(
                description='', schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description='Dùng để update, delete'),
                        "content": openapi.Schema(type=openapi.TYPE_STRING),
                        "rating": openapi.Schema(type=openapi.TYPE_NUMBER),
                        "course_instructor": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "reviewer": openapi.Schema(type=openapi.TYPE_INTEGER)
                    }
                )
            ),
            HTTP_400_BAD_REQUEST: openapi.Response(
                description='',
                examples={
                    'status': ['Missing one of content, rating, instructor, course, reviewer',
                               'Invalid rating!']
                }
            ),
            HTTP_404_NOT_FOUND: openapi.Response(
                description='',
                examples={
                    'status': 'CourseInstructor matching query does not exist'
                }
            ),
            HTTP_406_NOT_ACCEPTABLE: openapi.Response(
                description='',
                examples={
                    'status': 'User has already reviewed this instructor on this course'
                }
            )
        }
    )
    def create(self, request):
        content, rating, instructor, course, reviewer = data_from_method_post_put_delete(
            request,
            'content', 'rating', 'instructor', 'course', 'reviewer'
        )
        if none_any([content, rating, instructor, course, reviewer]):
            return Response(data={'status': 'Missing one of content, rating, instructor, course, reviewer'},
                            status=HTTP_400_BAD_REQUEST)
        if int(rating) > 5:
            return Response(data={'status': 'Invalid rating!'}, status=HTTP_400_BAD_REQUEST)
        try:
            # Check user joined this course
            if not JoinedCourse.objects.filter(Q(course_id=course) & Q(user_id=request.user.id)).exists():
                return Response(data={
                    'status': 'User not yet joined this course'
                }, status=HTTP_403_FORBIDDEN)

            course_instructor = CourseInstructor.objects.get(Q(course_id=course) & Q(user_id=instructor)).id
            # Check  if user has already review the instructor on this course
            if ReviewInstructor.objects.filter(
                    Q(course_instructor_id=course_instructor) & Q(reviewer_id=request.user.id)).exists():
                return Response(data={
                    'status': 'User has already reviewed this instructor on this course'
                }, status=HTTP_406_NOT_ACCEPTABLE)
            review_instructor_serializer = ReviewInstructorSerializer(data={
                'content': content, 'rating': rating, 'course_instructor': course_instructor, 'reviewer': reviewer
            })
            # Send notification to instructor
            send_notification(
                _type='system', to_user=instructor, location='hschool',
                title='New reviewed by student', content='You have new reviewed by student'
            )
            if review_instructor_serializer.is_valid():
                review_instructor_serializer.save()

                # push push_activity_log
                # push_activity_log
                return Response(data=review_instructor_serializer.data, status=HTTP_201_CREATED)
            else:
                return Response(data=review_instructor_serializer.errors, status=HTTP_201_CREATED)
        except (CourseInstructor.DoesNotExist, JoinedCourse.DoesNotExist, Exception) as e:
            if len(e.args) == 2:
                msg, code = e.args
            else:
                msg, code = e.args, None
            return Response(data={'status': f'{msg}'}, status=code if code is not None else HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description='Cập nhật review cho một instructor',
        operation_summary='Cập nhật review cho một instructor',
        manual_parameters=[
            openapi.Parameter('id', description='Id của review', in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'content': openapi.Schema(description='Nội dung review', type=openapi.TYPE_STRING),
                'rating': openapi.Schema(description='Rating giảng viên', type=openapi.TYPE_NUMBER),
            }
        ),
        responses={
            HTTP_200_OK: openapi.Response(
                description='', examples={
                    'status': 'Updated!'
                }
            ),
            HTTP_403_FORBIDDEN: openapi.Response(
                description='', examples={
                    'status': 'Failed!',
                    'msg': 'Do not have permission!'
                }
            ),
            HTTP_400_BAD_REQUEST: openapi.Response(
                description='', examples={
                    'status': ['Invalid rating!', 'Missing rating or invalid rating', 'Missing content']
                }
            ),
            HTTP_404_NOT_FOUND: openapi.Response(
                description='', examples={
                    'status': 'Not found!'
                }
            )
        }
    )
    def update(self, request, pk=None):
        try:
            review_instructor = ReviewInstructor.objects.get(pk=pk)
            # Check if has enough permission to delete
            # If user sent request is owner of the review or admin of the course
            if request.user.id == review_instructor.reviewer.id:
                content, rating = data_from_method_post_put_delete(request,
                                                                   'content', 'rating')
                if rating is None or rating == '':
                    return Response(data={'status': 'Missing rating or invalid rating'}, status=HTTP_400_BAD_REQUEST)
                if content is None:
                    return Response(data={'status': 'Missing content'}, status=HTTP_400_BAD_REQUEST)
                # Check if value is valid or not
                if int(rating) > 5:
                    return Response(data={'status': 'Invalid rating!'}, status=HTTP_400_BAD_REQUEST)
                review_instructor.content = content
                review_instructor.rating = rating
                review_instructor.save()
            else:
                return Response(data={'status': 'Failed!',
                                      'msg': 'Do not have permission!'}, status=HTTP_403_FORBIDDEN)
            return Response(data={'status': 'Updated!'}, status=HTTP_200_OK)
        except ReviewInstructor.DoesNotExist:
            return Response(data={'status': 'Not found!'}, status=HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description='Xóa một review instructor của một khóa học',
        operation_summary='Xóa một review instructor của một khóa học',
        manual_parameters=[
            openapi.Parameter('id', description='Id của review', in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER)
        ],
        responses={
            HTTP_200_OK: openapi.Response(
                description='', examples={
                    'status': 'Deleted!'
                }
            ),
            HTTP_403_FORBIDDEN: openapi.Response(
                description='', examples={
                    'status': 'Failed!',
                    'msg': 'Do not have permission!'
                }
            ),
            HTTP_404_NOT_FOUND: openapi.Response(
                description='', examples={
                    'status': 'Not found!'
                }
            ),
        }
    )
    def destroy(self, request, pk=None):
        try:
            review_instructor = ReviewInstructor.objects.get(pk=pk)
            # Check if has enough permission to delete
            # If user sent request is owner of the review or admin of the course
            if request.user.id == review_instructor.reviewer.id:
                review_instructor.delete()
            else:
                return Response(data={'status': 'Failed!',
                                      'msg': 'Do not have permission!'}, status=HTTP_403_FORBIDDEN)
            return Response(data={'status': 'Deleted!'}, status=HTTP_200_OK)
        except (ReviewInstructor.DoesNotExist, Exception):
            return Response(data={'status': 'Not found!'}, status=HTTP_404_NOT_FOUND)


class ReviewsInstructorsViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description='Danh sách các nhận xét( reviews) của các giáo viên( instructors)',
        operation_summary='Danh sách các nhận xét( reviews) của các giáo viên( instructors)',
        manual_parameters=[
            Parameter(name='is_mine', in_=IN_QUERY, type=TYPE_BOOLEAN,
                      description='Trả về những review khóa học (Do người đang đăng nhập tạo)'),
        ],
        responses={
            HTTP_200_OK: openapi.Response(
                description='',
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "data": Schema(
                                type=TYPE_ARRAY,
                                items=Schema(
                                    type=TYPE_OBJECT,
                                    properties={
                                        "id": Schema(type=TYPE_INTEGER, description='Id của review'),
                                        "instructor_info": Schema(type=TYPE_OBJECT, properties={
                                            'id': Schema(type=TYPE_INTEGER, description='Id của user'),
                                            'username': Schema(type=TYPE_STRING),
                                            'picture': Schema(type=TYPE_STRING, format=FORMAT_URI),
                                            'email': Schema(type=TYPE_STRING, format=FORMAT_EMAIL),
                                            'url': Schema(type=TYPE_STRING, format=FORMAT_SLUG,
                                                          description='Url của user')
                                        }),
                                        "reviewer_info": Schema(type=TYPE_OBJECT, properties={
                                            'id': Schema(type=TYPE_INTEGER, description='Id của user'),
                                            'username': Schema(type=TYPE_STRING),
                                            'picture': Schema(type=TYPE_STRING, format=FORMAT_URI),
                                            'email': Schema(type=TYPE_STRING, format=FORMAT_EMAIL),
                                            'url': Schema(type=TYPE_STRING, format=FORMAT_SLUG,
                                                          description='Url của user')
                                        }),
                                        "course_info": Schema(type=TYPE_OBJECT, properties={
                                            'id': Schema(type=TYPE_INTEGER, description='Id của khóa học'),
                                            'title': Schema(type=TYPE_STRING),
                                            'picture': Schema(type=TYPE_STRING, format=FORMAT_URI),
                                            'slug': Schema(type=TYPE_STRING, format=FORMAT_SLUG,
                                                           description='Slug của khóa học')
                                        }),
                                        "content": Schema(type=TYPE_STRING),
                                        "rating": Schema(type=TYPE_NUMBER, format=FORMAT_FLOAT),
                                        "date_created": Schema(type=TYPE_STRING, format=FORMAT_DATETIME),
                                        "course_instructor": Schema(type=TYPE_INTEGER),
                                        "reviewer": Schema(type=TYPE_INTEGER),
                                    })
                            ),
                            "metadata": Schema(
                                type=TYPE_OBJECT,
                                properties={
                                    "valid_page": Schema(type=TYPE_BOOLEAN),
                                    "count": Schema(type=TYPE_BOOLEAN),
                                    "num_pages": Schema(type=TYPE_BOOLEAN),
                                    "page_range": Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_INTEGER)),
                                    "has_next": Schema(type=TYPE_BOOLEAN),
                                    "has_previous": Schema(type=TYPE_BOOLEAN),
                                    "current_page": Schema(type=TYPE_INTEGER),
                                    "next_page_number": Schema(type=TYPE_INTEGER),
                                    "previous_page_number": Schema(type=TYPE_INTEGER)
                                }
                            ),
                        }
                    )
                )
            )
        }
    )
    def list(self, request):
        try:
            # Get all instructor
            _reviews_instructors = ReviewInstructor.objects
            # Get reviews of my course
            if request.query_params.get('is_mine') and request.query_params.get('is_mine') == 'true':
                _reviews_instructors = _reviews_instructors.filter(
                    course_instructor__course__creator__id=request.user.id)
            _reviews_instructors = _reviews_instructors.order_by('-date_created')
            # Return information about instructor
            reviews_instructors, metadata = h_paginator(object_list=_reviews_instructors, request=request)
            reviews_instructors_serializers = ReviewInstructorSerializer(instance=reviews_instructors,
                                                                         many=True)
            context = {
                "data": reviews_instructors_serializers.data,
                "metadata": metadata
            }
            return Response(data=context, status=HTTP_200_OK)
        except (User.DoesNotExist, Exception) as e:
            if len(e.args) == 2:
                msg, code = e.args
            else:
                msg, code = e.args, None
            return Response(data={'status': f'{msg}'}, status=code if code is not None else HTTP_404_NOT_FOUND)


class CRUDSubCategoriesViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description='Danh sách course subcategory',
        operation_summary='Danh sách course subcategory',
        manual_parameters=[
            openapi.Parameter('category_id', type=TYPE_STRING, in_=openapi.IN_QUERY, description='Id category filter'),
        ],
        responses={
            HTTP_200_OK: openapi.Response(
                description='',
                schema=Schema(
                    type=TYPE_ARRAY,
                    items=CourseSubCategorySchema.data_out_schema()
                )
            ),
            HTTP_401_UNAUTHORIZED: openapi.Response(
                description='Lỗi 401 unauthorized',
                examples={
                    'status': 'failed',
                    'message': 'Kiểm tra lại email đăng nhập hoặc mặt khẩu'
                }
            )
        }
    )
    def list(self, request):
        all_subcategories = CourseSubCategory.objects.all()
        if request.query_params.get('category_id'):
            all_subcategories = all_subcategories.filter(category__id=request.query_params.get('category_id'))
        data_list = CourseSubCategorySerializer(all_subcategories, many=True).data
        return Response(data=data_list, status=HTTP_200_OK)

    @swagger_auto_schema(
        operation_description='Tạo mới course Subcategory',
        operation_summary='Tạo mới course Subcategory',
        request_body=CourseSubCategorySchema.data_in_schema(),
        responses={
            HTTP_200_OK: openapi.Response(
                description='',
                schema=CourseSubCategorySchema.data_out_schema()
            ),
            HTTP_404_NOT_FOUND: openapi.Response(
                description='', schema=Schema(type=TYPE_OBJECT, properties={
                    'message': Schema(type=TYPE_STRING)
                }),
                examples={
                    'message': 'Does not exist',
                }
            ),
            HTTP_401_UNAUTHORIZED: openapi.Response(
                description='Lỗi 401 unauthorized',
                examples={
                    'status': 'failed',
                    'message': 'Kiểm tra lại email đăng nhập hoặc mặt khẩu'
                }
            )
        }
    )
    def create(self, request):
        course_subcategory_serializer = CourseSubCategorySerializer(data={
            'category': request.data.get('category'),
            'name': request.data.get('name'),
            'thumb': request.data.get('thumb')
        }, context={'request': request})
        if course_subcategory_serializer.is_valid():
            course_subcategory_serializer.save()

            if request.data.get('area'):
                course_subcategory = CourseSubCategory.objects.get(pk=course_subcategory_serializer.data['id'])
                for area in json.loads(request.data.get('area')):
                    if 'id' in area.keys() and area['id']:
                        course_subcategory.area.add(area['id'])
                    else:
                        _area = Area.objects.create(name=area['name'])
                        course_subcategory.area.add(_area)
            data = CourseSubCategorySerializer(
                CourseSubCategory.objects.get(pk=course_subcategory_serializer.data['id']))
            return Response(data={'data': data.data, 'status': 'created'}, status=HTTP_201_CREATED)
        return Response(data=course_subcategory_serializer.errors, status=HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description='Cập nhật course Subcategory',
        operation_summary='Cập nhật course Subcategory',
        request_body=CourseSubCategorySchema.data_in_schema(),
        responses={
            HTTP_200_OK: openapi.Response(
                description='',
                schema=CourseSubCategorySchema.data_out_schema()
            ),
            HTTP_404_NOT_FOUND: openapi.Response(
                description='', schema=Schema(type=TYPE_OBJECT, properties={
                    'message': Schema(type=TYPE_STRING)
                }),
                examples={
                    'message': 'Does not exist',
                }
            ),
            HTTP_401_UNAUTHORIZED: openapi.Response(
                description='Lỗi 401 unauthorized',
                examples={
                    'status': 'failed',
                    'message': 'Kiểm tra lại email đăng nhập hoặc mặt khẩu'
                }
            )
        }
    )
    def update(self, request, pk=None):

        try:
            course_subcategory_instance = CourseSubCategory.objects.get(pk=pk)

            data_put = {}
            if request.data.get('category'):
                data_put['category'] = request.data.get('category')
            if request.data.get('name'):
                data_put['name'] = request.data.get('name')

            if not request.FILES.getlist('thumb'):
                request.POST._mutable = True
                del request.data['thumb']
                request.POST._mutable = False
            else:
                if request.data.get('thumb'):
                    data_put['thumb'] = request.data.get('thumb')
            course_subcategory_serializer = CourseSubCategorySerializer(
                instance=course_subcategory_instance,
                data=data_put, context={'request': request}, partial=True)
            if course_subcategory_serializer.is_valid():
                course_subcategory_serializer.save()

                if request.data.get('area'):
                    course_subcategory_instance.area.clear()
                    for area in json.loads(request.data.get('area')):
                        if 'id' in area.keys() and area['id']:
                            course_subcategory_instance.area.add(area['id'])
                        else:
                            _area = Area.objects.create(name=area['name'])
                            course_subcategory_instance.area.add(_area)
                data = CourseSubCategorySerializer(
                    CourseSubCategory.objects.get(pk=course_subcategory_serializer.data['id']))
                return Response(data={'data': data.data, 'status': 'updated'}, status=HTTP_200_OK)
            return Response(data=course_subcategory_serializer.errors, status=HTTP_400_BAD_REQUEST)
        except (CourseSubCategory.DoesNotExist, Exception) as e:
            if len(e.args) == 2:
                msg, code = e.args
            else:
                msg, code = e.args, None
            return Response(data={'status': f'{msg}'}, status=code if code is not None else HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description='Xóa course subcategory',
        operation_summary='Xóa course subcategory',
        responses={
            HTTP_200_OK: openapi.Response(
                description='',
                schema=Schema(
                    type=TYPE_OBJECT,
                    properties={
                        "status": Schema(type=TYPE_STRING),
                    }

                )
            ),
            HTTP_404_NOT_FOUND: openapi.Response(
                description='', schema=Schema(type=TYPE_OBJECT, properties={
                    'message': Schema(type=TYPE_STRING)
                }),
                examples={
                    'message': 'Does not exist',
                }
            ),
            HTTP_401_UNAUTHORIZED: openapi.Response(
                description='Lỗi 401 unauthorized',
                examples={
                    'status': 'failed',
                    'message': 'Kiểm tra lại email đăng nhập hoặc mặt khẩu'
                }
            ),
            HTTP_403_FORBIDDEN: openapi.Response(
                description='Lỗi 403 Forbidden',
                examples={
                    'status': 'Permission Denied'
                }
            )
        }
    )
    def destroy(self, request, pk=None):
        try:
            instance = CourseSubCategory.objects.get(pk=pk)
            instance.delete()
            return Response(data={'status': 'delete'}, status=HTTP_200_OK)
        except (CourseSubCategory.DoesNotExist, Type.DoesNotExist, Exception) as e:
            if len(e.args) == 2:
                msg, code = e.args
            else:
                msg, code = e.args, None
            return Response(data={'status': f'{msg}'}, status=code if code is not None else HTTP_404_NOT_FOUND)


class CRUDAreasViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description='Tạo skill mới',
        operation_summary='Tạo skill mới',
        request_body=Schema(
            type=TYPE_OBJECT,
            description='Dùng formData',
            properties={
                'area_name': Schema(type=TYPE_STRING),
                'list_type_id': Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_STRING),
                                       description='List id của sub category'),
            }),
        responses={
            HTTP_200_OK: openapi.Response(
                description='',
                schema=Schema(
                    type=TYPE_OBJECT,
                    properties={
                        "data": Schema(
                            type=TYPE_OBJECT,
                            properties={
                                "id": Schema(type=TYPE_INTEGER),
                                "name": Schema(type=TYPE_STRING),
                                "types": Schema(type=TYPE_ARRAY,
                                                items=Schema(type=TYPE_STRING, description='Array types'))
                            }),
                        "status": Schema(type=TYPE_STRING)
                    }
                )
            ),
            HTTP_404_NOT_FOUND: openapi.Response(
                description='', schema=Schema(type=TYPE_OBJECT, properties={
                    'message': Schema(type=TYPE_STRING)
                }),
                examples={
                    'message': 'Does not exist',
                }
            ),
            HTTP_401_UNAUTHORIZED: openapi.Response(
                description='Lỗi 401 unauthorized',
                examples={
                    'status': 'failed',
                    'message': 'Kiểm tra lại email đăng nhập hoặc mặt khẩu'
                }
            )
        }
    )
    def create(self, request):
        area_name, list_type_id = data_from_method_post_put_delete(
            request,
            'area_name',
            'list_type_id',
        )

        try:
            # Query list course category -> get type id
            list_sub_categories = CourseCategory.objects.filter(id__in=json.loads(list_type_id)).values_list('type',
                                                                                                             flat=True)
            # Serializer type
            area_serializer = AreaSerializer(data={
                'name': area_name,
                'types': [sub_category for sub_category in list_sub_categories],
            })
            # Check type is valid?
            if area_serializer.is_valid():
                area_serializer.save()
                return Response(data={'data': area_serializer.data, 'status': 'Created!'},
                                status=HTTP_201_CREATED)
            return Response(data=area_serializer.errors, status=HTTP_400_BAD_REQUEST)
        except (CourseCategory.DoesNotExist, Area.DoesNotExist, Exception) as e:
            if len(e.args) == 2:
                msg, code = e.args
            else:
                msg, code = e.args, None
            return Response(data={'status': f'{msg}'}, status=code if code is not None else HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description='Cập nhập skill',
        operation_summary='Cập nhập skill',
        request_body=Schema(
            type=TYPE_OBJECT,
            description='Dùng formData',
            properties={
                'area_id': Schema(type=TYPE_STRING),
                'area_name': Schema(type=TYPE_STRING),
                'list_type_id': Schema(
                    type=TYPE_ARRAY, items=Schema(type=TYPE_STRING),
                    description='List id của sub category'
                ),
            }),
        responses={
            HTTP_200_OK: openapi.Response(
                description='',
                schema=Schema(
                    type=TYPE_OBJECT,
                    properties={
                        "data": Schema(
                            type=TYPE_OBJECT,
                            properties={
                                "id": Schema(type=TYPE_INTEGER),
                                "name": Schema(type=TYPE_STRING),
                                "types": Schema(type=TYPE_ARRAY,
                                                items=Schema(type=TYPE_STRING, description='Array types'))
                            }),
                        "status": Schema(type=TYPE_STRING)
                    }
                )
            ),
            HTTP_404_NOT_FOUND: openapi.Response(
                description='', schema=Schema(type=TYPE_OBJECT, properties={
                    'message': Schema(type=TYPE_STRING)
                }),
                examples={
                    'message': 'Does not exist',
                }
            ),
            HTTP_401_UNAUTHORIZED: openapi.Response(
                description='Lỗi 401 unauthorized',
                examples={
                    'status': 'failed',
                    'message': 'Kiểm tra lại email đăng nhập hoặc mặt khẩu'
                }
            )
        }
    )
    def update(self, request, pk=None):
        area_id, area_name, list_type_id = data_from_method_post_put_delete(
            request,
            'area_id',
            'area_name',
            'list_type_id',
        )

        try:

            # Query list course category -> get type id
            list_sub_categories = CourseCategory.objects.filter(id__in=json.loads(list_type_id)).values_list('type',
                                                                                                             flat=True)

            area = Area.objects.get(id=area_id)
            # Serializer type
            area_serializer = AreaSerializer(data={
                'name': area_name,
                'types': [sub_category for sub_category in list_sub_categories],
            }, instance=area, partial=True)

            # Check type is valid?
            if area_serializer.is_valid():
                area_serializer.save()
                return Response(data={'data': area_serializer.data, 'status': 'Updated!'},
                                status=HTTP_201_CREATED)
            return Response(data=area_serializer.errors, status=HTTP_400_BAD_REQUEST)
        except (CourseCategory.DoesNotExist, Area.DoesNotExist, Exception) as e:
            if len(e.args) == 2:
                msg, code = e.args
            else:
                msg, code = e.args, None
            return Response(data={'status': f'{msg}'}, status=code if code is not None else HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description='Xóa skill',
        operation_summary='Xóa skill',
        responses={
            HTTP_200_OK: openapi.Response(
                description='',
                schema=Schema(
                    type=TYPE_OBJECT,
                    properties={
                        "status": Schema(type=TYPE_STRING),
                    }

                )
            ),
            HTTP_404_NOT_FOUND: openapi.Response(
                description='', schema=Schema(type=TYPE_OBJECT, properties={
                    'message': Schema(type=TYPE_STRING)
                }),
                examples={
                    'message': 'Does not exist',
                }
            ),
            HTTP_401_UNAUTHORIZED: openapi.Response(
                description='Lỗi 401 unauthorized',
                examples={
                    'status': 'failed',
                    'message': 'Kiểm tra lại email đăng nhập hoặc mặt khẩu'
                }
            ),
            HTTP_403_FORBIDDEN: openapi.Response(
                description='Lỗi 403 Forbidden',
                examples={
                    'status': 'Permission Denied'
                }
            )
        }
    )
    def destroy(self, request, pk=None):
        try:
            _a = Area.objects.get(pk=pk)
            _a.delete()
            return Response(data={'status': 'Deleted!'}, status=HTTP_200_OK)
        except (Area.DoesNotExist, Exception) as e:
            if len(e.args) == 2:
                msg, code = e.args
            else:
                msg, code = e.args, None
            return Response(data={'status': f'{msg}'}, status=code if code is not None else HTTP_404_NOT_FOUND)


class ReviewsMeViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description='Danh sách các nhận xét( reviews) của tôi',
        operation_summary='Danh sách các nhận xét( reviews) của tôi',
        responses={
            HTTP_200_OK: openapi.Response(
                description='',
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "data": Schema(
                                type=TYPE_ARRAY,
                                items=Schema(
                                    type=TYPE_OBJECT,
                                    properties={
                                        "id": Schema(type=TYPE_INTEGER),
                                        "content": Schema(type=TYPE_STRING),
                                        "rating": Schema(type=TYPE_NUMBER, format=FORMAT_FLOAT),
                                        "date_created": Schema(type=TYPE_STRING, format=FORMAT_DATETIME),
                                        "course_instructor": Schema(type=TYPE_INTEGER),
                                        "type": Schema(type=TYPE_STRING),
                                    })
                            ),
                            "metadata": Schema(
                                type=TYPE_OBJECT,
                                properties={
                                    "valid_page": Schema(type=TYPE_BOOLEAN),
                                    "count": Schema(type=TYPE_BOOLEAN),
                                    "num_pages": Schema(type=TYPE_BOOLEAN),
                                    "page_range": Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_INTEGER)),
                                    "has_next": Schema(type=TYPE_BOOLEAN),
                                    "has_previous": Schema(type=TYPE_BOOLEAN),
                                    "current_page": Schema(type=TYPE_INTEGER),
                                    "next_page_number": Schema(type=TYPE_INTEGER),
                                    "previous_page_number": Schema(type=TYPE_INTEGER)
                                }
                            ),
                        }
                    )
                )
            )
        }
    )
    def list(self, request):
        try:
            # Get review
            all_review_course = CourseRating.objects.filter(
                user_id=request.user.id).annotate(
                type=Concat('user_id', Value(' course '), 'course_id', output_field=CharField()),
                _rating=F('num_star')).values('id', 'content', 'date_created', '_rating', 'type').order_by(
                '-date_created')
            all_review_instructor = ReviewInstructor.objects.annotate(
                type=Concat('reviewer_id', Value(' instructor '), 'course_instructor_id', output_field=CharField()),
                _rating=F('rating')
            ).filter(reviewer_id=request.user.id).values(
                'id', 'content', 'date_created', '_rating', 'type').order_by('-date_created')
            # Chain all review
            _all_reviews = all_review_course.union(all_review_instructor)

            # Get all in one page if not limit in request
            count_pagination = _all_reviews.count()
            if not request.GET.get('limit'):
                if not request.GET._mutable:
                    request.GET._mutable = True
                request.GET['limit'] = count_pagination

            all_reviews, metadata = h_paginator(object_list=_all_reviews, request=request)

            data = []
            for rv in all_reviews:
                _obj = {
                    'id': rv['id'],
                    'content': rv['content'],
                    'date_created': rv['date_created'],
                    'rating': rv['_rating'],
                    'type': 'instructor' if 'instructor' in rv['type'] else 'course',
                }
                c = None
                if 'course' in rv['type']:
                    c = Course.objects.get(id=rv['type'].split(' ')[2])

                elif 'instructor' in rv['type']:
                    u = User.objects.get(id=rv['type'].split(' ')[0])
                    _obj_u = {
                        'id': u.id,
                        'username': u.username,
                        'avatar': u.picture.build_url() if u.picture else ''
                    }
                    _obj['instructor'] = _obj_u
                    ci = CourseInstructor.objects.get(pk=rv['type'].split(' ')[2])
                    c = Course.objects.get(pk=ci.course_id)

                if c:
                    _c_obj = {
                        'id': c.id,
                        'title': c.title,
                        'thumb': c.thumb.build_url() if c.thumb else '',
                    }
                    _obj['course'] = _c_obj
                data.append(_obj)
            context = {
                "data": data,
                "metadata": metadata
            }
            return Response(data=context, status=HTTP_200_OK)
        except (User.DoesNotExist, CourseInstructor.DoesNotExist, Course.DoesNotExist, Exception) as e:
            if len(e.args) == 2:
                msg, code = e.args
            else:
                msg, code = e.args, None
            return Response(data={'status': f'{msg}'}, status=code if code is not None else HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description='Xóa rating của tôi',
        operation_summary='Xóa rating của tôi',
        request_body=Schema(
            type=TYPE_OBJECT,
            properties={
                "type": Schema(description='Loại rating muốn xóa: instructor hoặc course', type=TYPE_STRING,
                               default='course'),
            }
        ),
        responses={
            HTTP_200_OK: openapi.Response(
                description='',
                schema=Schema(
                    type=TYPE_OBJECT,
                    properties={
                        "status": Schema(type=TYPE_STRING),
                    }

                )
            ),
            HTTP_404_NOT_FOUND: openapi.Response(
                description='', schema=Schema(type=TYPE_OBJECT, properties={
                    'message': Schema(type=TYPE_STRING)
                }),
                examples={
                    'message': 'Does not exist',
                }
            ),
            HTTP_401_UNAUTHORIZED: openapi.Response(
                description='Lỗi 401 unauthorized',
                examples={
                    'status': 'failed',
                    'message': 'Kiểm tra lại email đăng nhập hoặc mặt khẩu'
                }
            ),
            HTTP_403_FORBIDDEN: openapi.Response(
                description='Lỗi 403 Forbidden',
                examples={
                    'status': 'Permission Denied'
                }
            )
        }
    )
    def destroy(self, request, pk=None):
        try:
            _type, = data_from_method_post_put_delete(request, 'type')
            if 'course' in _type:
                cr = CourseRating.objects.get(pk=pk)
                if cr.user.id != request.user.id:
                    return Response(data={'status': 'Forbidden!'}, status=HTTP_403_FORBIDDEN)
                cr.delete()
            elif 'instructor' in _type:
                ri = ReviewInstructor.objects.get(pk=pk)
                if ri.reviewer.id != request.user.id:
                    return Response(data={'status': 'Forbidden!'}, status=HTTP_403_FORBIDDEN)
                ri.delete()
            return Response(data={'status': 'Deleted!'}, status=HTTP_200_OK)
        except (CourseRating.DoesNotExist, ReviewInstructor.DoesNotExist, Exception) as e:
            if len(e.args) == 2:
                msg, code = e.args
            else:
                msg, code = e.args, None
            return Response(data={'status': f'{msg}'}, status=code if code is not None else HTTP_404_NOT_FOUND)


class InstructorAcceptInvitation(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description='Chấp nhận lời mời dạy khóa học',
        operation_summary='Chấp nhận lời mời dạy khóa học',
        request_body=Schema(
            type=TYPE_OBJECT,
            properties={
                "course_id": Schema(type=TYPE_INTEGER, description='Id của khóa học hiện tại'),
                "user_id": Schema(type=TYPE_INTEGER, description='Id của user(instructor) người được mời'),
                "view_as_id": Schema(type=TYPE_INTEGER, description='Id của người được mời( Kèm tại email)'),
            }
        ),
        responses={
            HTTP_200_OK: openapi.Response(
                description='Cập nhập thành công',
                schema=Schema(
                    type=TYPE_OBJECT,
                    properties={
                        "status": Schema(type=TYPE_STRING),
                    }
                )
            ),
            HTTP_400_BAD_REQUEST: openapi.Response(
                description='Bad request',
                schema=Schema(
                    type=TYPE_OBJECT, properties={
                        "message": Schema(type=TYPE_STRING),
                    }
                )
            ),
            HTTP_404_NOT_FOUND: openapi.Response(
                description='Lỗi không tìm thấy',
                schema=Schema(
                    type=TYPE_OBJECT, properties={
                        "message": Schema(type=TYPE_STRING),
                    }
                )
            ),
            HTTP_401_UNAUTHORIZED: openapi.Response(
                description='Lỗi trả về',
                examples={
                    'status': 'failed',
                    'message': 'Kiểm tra lại email đăng nhập hoặc mặt khẩu'
                }
            )
        }

    )
    def put(self, request, pk=None):
        course_id, user_id, view_as_id, _type = data_from_method_post_put_delete(request, 'course_id', 'user_id',
                                                                                 'view_as_id', 'type')
        try:
            # Get the course from db
            user = User.objects.get(pk=view_as_id)
            if request.user.id != user.id:
                raise Exception('Do not have permission', HTTP_403_FORBIDDEN)

            # Update invite or update apply teaching
            invite = None
            at = None
            if _type and 'invite' in _type:
                is_invite = Invitation.objects.filter(course_id=course_id, to_user_id=user_id,
                                                      is_accepted=False).values_list('to_user', flat=True)
                if request.user.id not in is_invite:
                    raise Exception('Do not have permission', HTTP_403_FORBIDDEN)

                invite = Invitation.objects.filter(course_id=course_id, to_user_id=user_id, is_accepted=False).first()
                invite.is_accepted = True
                invite.save()
            elif _type and 'apply' in _type:
                is_apply = ApplyTeaching.objects.filter(course_id=course_id, user_id=user_id, is_accepted=False).first()
                if is_apply.course.creator_id != request.user.id:
                    return Response(data={'status': 'Permission Denied'}, status=HTTP_403_FORBIDDEN)

                at = ApplyTeaching.objects.filter(course_id=course_id, user_id=user_id, is_accepted=False).first()
                at.is_accepted = True
                at.save()

            if invite or at:
                CourseInstructor.objects.create(course_id=course_id, user_id=user_id, rating=0, fee=0)

            return Response(data={"status": "Accepted"}, status=HTTP_200_OK)
        except (Course.DoesNotExist, Exception) as e:
            if len(e.args) == 2:
                msg, code = e.args
            else:
                msg, code = e.args, None
            return Response(data={'status': f'{msg}'}, status=code if code is not None else HTTP_404_NOT_FOUND)


class CRUDCategoriesViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description='Danh sách course category',
        operation_summary='Danh sách course category',
        manual_parameters=[
            openapi.Parameter('page', type=TYPE_INTEGER, in_=openapi.IN_QUERY, description='Trang'),
            openapi.Parameter('limit', type=TYPE_INTEGER, in_=openapi.IN_QUERY, description='Số items trên 1 trang'),
            openapi.Parameter('q', type=TYPE_STRING, in_=openapi.IN_QUERY, description='Tìm kiếm theo từ khóa (name,...)')
        ],
        responses={
            HTTP_200_OK: openapi.Response(
                description='',
                schema=Schema(
                    type=TYPE_ARRAY,
                    items=CourseCategorySchema.out_schema()
                )
            ),
            HTTP_401_UNAUTHORIZED: openapi.Response(
                description='Lỗi 401 unauthorized',
                examples={
                    'status': 'failed',
                    'message': 'Kiểm tra lại email đăng nhập hoặc mặt khẩu'
                }
            )
        }
    )
    def list(self, request):
        course_categories = CourseCategory.objects.all()
        # search by q
        if request.GET.get('q'):
            course_categories = course_categories.filter(name__icontains=request.GET.get('q'))
        # edit limit
        request.GET._mutable = True
        limit = course_categories.count() if not request.GET.get('limit') else request.GET.get('limit')
        if not course_categories.count() and not not request.GET.get('limit'):
            limit = None
        request.GET['limit'] = limit
        request.GET._mutable = False
        data, metadata = h_paginator(object_list=course_categories, request=request)
        data_list = CourseCategorySerializer(data, many=True).data
        return Response(data={'data': data_list, 'metadata': metadata}, status=HTTP_200_OK)

    @swagger_auto_schema(
        operation_description='Tạo mới course category',
        operation_summary='Tạo mới course category',
        request_body=CourseCategorySchema.data_schema(),
        responses={
            HTTP_200_OK: openapi.Response(
                description='',
                schema=Schema(
                    type=TYPE_ARRAY,
                    items=CourseCategorySchema.out_schema()
                )
            ),
            HTTP_401_UNAUTHORIZED: openapi.Response(
                description='Lỗi 401 unauthorized',
                examples={
                    'status': 'failed',
                    'message': 'Kiểm tra lại email đăng nhập hoặc mặt khẩu'
                }
            )
        }
    )
    def create(self, request):
        # check if admin( người tạo có quyền tạo course category)
        course_category_serializer = CourseCategorySerializer(data=request.data, context={'request': request})
        if course_category_serializer.is_valid():
            course_category_serializer.save()

            return Response(data={'status': 'created', 'data': course_category_serializer.data},
                            status=HTTP_201_CREATED)
        else:
            return Response(data={'status': 'failed', 'msg': course_category_serializer.errors},
                            status=HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description='Cập nhật course category',
        operation_summary='Cập nhật course category',
        request_body=CourseCategorySchema.data_schema(),
        responses={
            HTTP_200_OK: openapi.Response(
                description='',
                schema=Schema(
                    type=TYPE_ARRAY,
                    items=CourseCategorySchema.out_schema()
                )
            ),
            HTTP_401_UNAUTHORIZED: openapi.Response(
                description='Lỗi 401 unauthorized',
                examples={
                    'status': 'failed',
                    'message': 'Kiểm tra lại email đăng nhập hoặc mặt khẩu'
                }
            )
        }
    )
    def update(self, request, pk=None):
        # check if admin( người tạo có quyền tạo course category)
        # get instance
        try:
            course_category_instance = CourseCategory.objects.get(pk=pk)
            if not request.FILES.getlist('thumb'):
                request.POST._mutable = True
                del request.data['thumb']
                request.POST._mutable = False
            course_category_serializer = CourseCategorySerializer(instance=course_category_instance, data=request.data,
                                                                  context={'request': request}, partial=True)
            if course_category_serializer.is_valid():
                course_category_serializer.save()

                return Response(data={'status': 'updated', 'data': course_category_serializer.data},
                                status=HTTP_200_OK)
            else:
                return Response(data={'status': 'failed', 'msg': course_category_serializer.errors},
                                status=HTTP_400_BAD_REQUEST)
        except CourseCategory.DoesNotExist as e:
            if len(e.args) == 2:
                msg, code = e.args
            else:
                msg, code = e.args, None
            return Response(data={'status': 'failed', 'message': f'{msg}'},
                            status=code if code is not None else HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description='Chi tiết course category',
        operation_summary='Chi tiết course category',
        responses={
            HTTP_200_OK: openapi.Response(
                description='',
                schema=Schema(
                    type=TYPE_ARRAY,
                    items=CourseCategorySchema.out_schema()
                )
            ),
            HTTP_401_UNAUTHORIZED: openapi.Response(
                description='Lỗi 401 unauthorized',
                examples={
                    'status': 'failed',
                    'message': 'Kiểm tra lại email đăng nhập hoặc mặt khẩu'
                }
            )
        }
    )
    def retrieve(self, request, pk=None):
        # check if admin( người tạo có quyền tạo course category)
        # get instance
        try:
            course_category_instance = CourseCategory.objects.get(pk=pk)
            course_category_serializer = CourseCategorySerializer(instance=course_category_instance,
                                                                  context={'request': request})

            return Response(data=course_category_serializer.data, status=HTTP_200_OK)
        except CourseCategory.DoesNotExist as e:
            if len(e.args) == 2:
                msg, code = e.args
            else:
                msg, code = e.args, None
            return Response(data={'status': 'failed', 'message': f'{msg}'},
                            status=code if code is not None else HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description='Xóa course category',
        operation_summary='Xóa course category',
        responses={
            HTTP_200_OK: openapi.Response(
                description='',
                schema=Schema(
                    type=TYPE_OBJECT,
                    properties={
                        "status": Schema(type=TYPE_STRING),
                    }

                )
            ),
            HTTP_404_NOT_FOUND: openapi.Response(
                description='', schema=Schema(type=TYPE_OBJECT, properties={
                    'message': Schema(type=TYPE_STRING)
                }),
                examples={
                    'message': 'Does not exist',
                }
            ),
            HTTP_401_UNAUTHORIZED: openapi.Response(
                description='Lỗi 401 unauthorized',
                examples={
                    'status': 'failed',
                    'message': 'Kiểm tra lại email đăng nhập hoặc mặt khẩu'
                }
            ),
            HTTP_403_FORBIDDEN: openapi.Response(
                description='Lỗi 403 Forbidden',
                examples={
                    'status': 'Permission Denied'
                }
            )
        }
    )
    def destroy(self, request, pk=None):
        try:
            instance = CourseCategory.objects.get(pk=pk)
            instance.delete()
            return Response(data={'status': 'Deleted'}, status=HTTP_200_OK)
        except (CourseCategory.DoesNotExist, Exception) as e:
            if len(e.args) == 2:
                msg, code = e.args
            else:
                msg, code = e.args, None
            return Response(data={'status': f'{msg}'}, status=code if code is not None else HTTP_404_NOT_FOUND)
