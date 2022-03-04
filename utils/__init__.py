#  Copyright (c) 2020.
#  Team hspaces.net
#  Contributors sang.tanhle, HuynhDH
import logging
import secrets
import socket
from typing import Type

import cloudinary.api
from django.db.models import QuerySet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from models.media import Media

logger = logging.getLogger(__name__)


def none_any(*args):
    """
    Kiểm tra 1 trong các đối số là None
    :param args:
    :return: True or False
    """
    for arg in args:
        if arg is None or arg == '':
            return True
    return False


def number_of_not_none_args(*args):
    """Number of not None args"""
    count = 0
    for arg in args:
        if arg is None:
            count += 1
    return count


def name_of_none_args(args: list, args_name: list) -> list:
    """Return name of arg has value equal None
    Args:
        args: List of args value
        args_name: List of args name
    Raises:
        ValueError: args with args_name must be same size
    Returns:
        args_name: List of args has None value
    """
    if len(args) != len(args_name):
        raise ValueError('args with args_name must be same size')
    none_args_name = []
    for arg, arg_name in zip(args, args_name):
        if arg is None:
            none_args_name.append(arg_name)
    return none_args_name


def update_cover(medias: QuerySet, cover_img, current_owner_id=None, _type=None, success_code=201):
    """
    Cập nhật ảnh bìa
    :param medias:
    :param cover_img:
    :param current_owner_id:
    :param _type:
    :param success_code:
    :return:
    """
    # Update image cover when existed one or more
    if medias.exists():
        try:
            cover_url = None
            for m in medias:
                if m.media_type == 'img' and m.image is not None:
                    cloudinary.api.delete_resources(m.image.public_id)
                    m.image = None
                elif m.media_type == 'vid':
                    m.url = None
                    m.media_type = 'img'
                m.image = cover_img
                m.save()
                # Build cover url an response back to client
                cover_url = m.image.build_url(
                    secure=True,
                    crop='thumb') if m.image is not None else None
            return Response(data={'status': 'success', 'cover_url': cover_url}, status=success_code)
        except (AttributeError, Exception):
            return Response(data={'status': "An error happened during upload cover!"}, status=HTTP_400_BAD_REQUEST)
    # Create new one if there isn't existed
    if _type == 'user':
        media = Media.objects.create(user_id=current_owner_id, image=cover_img, set_as_cover=True, media_type='img')
        cover_url = media.image.build_url(
            secure=True,
            crop='thumb') if media.image is not None else None
        return Response(data={'status': 'success', 'cover_url': cover_url}, status=success_code)

    if _type == 'team/startup':
        media = Media.objects.create(team_id=current_owner_id, image=cover_img, set_as_cover=True, media_type='img')
        cover_url = media.image.build_url(
            secure=True,
            crop='thumb') if media.image is not None else None
        return Response(data={'status': 'success', 'cover_url': cover_url}, status=success_code)

    if _type == 'org':
        media = Media.objects.create(organization_id=current_owner_id, image=cover_img, set_as_cover=True,
                                     media_type='img')
        cover_url = media.image.build_url(
            secure=True,
            crop='thumb') if media.image is not None else None
        return Response(data={'status': 'success', 'cover_url': cover_url}, status=success_code)

    if _type == 'contest':
        media = Media.objects.create(contest_id=current_owner_id, image=cover_img, set_as_cover=True, media_type='img')
        cover_url = media.image.build_url(
            secure=True,
            crop='thumb') if media.image is not None else None
        return Response(data={'status': 'success', 'cover_url': cover_url}, status=success_code)

    if _type == 'event':
        media = Media.objects.create(event_id=current_owner_id, image=cover_img, set_as_cover=True, media_type='img')
        cover_url = media.image.build_url(
            secure=True,
            crop='thumb') if media.image is not None else None
        return Response(data={'status': 'success', 'cover_url': cover_url}, status=success_code)

    if _type == 'post':
        Media.objects.create(post_id=current_owner_id, image=cover_img, set_as_cover=True, media_type='img')
        return Response(data={'status': 'success'}, status=success_code)


def update_video_cover(medias: QuerySet, cover_youtube_video_url, current_owner_id=None, _type=None, success_code=201):
    """
    Cập nhật video bìa cho trang
    :param medias:
    :param cover_youtube_video_url:
    :param current_owner_id:
    :param _type:
    :param success_code:
    :return:
    """
    if medias.exists():
        for m in medias:
            try:
                if m.media_type == 'img' and m.image is not None:
                    cloudinary.api.delete_resources(m.image.public_id)
                    m.image = None
                m.media_type = 'vid'
                m.url = cover_youtube_video_url
                m.save()
                return Response(data={'status': 'success'}, status=success_code)
            except (AttributeError, Exception) as e:
                return Response(data={'status': e}, status=HTTP_400_BAD_REQUEST)
        return

    if _type == 'user':
        Media.objects.create(user_id=current_owner_id, url=cover_youtube_video_url, set_as_cover=True, media_type='vid')
        return Response(data={'status': 'success'}, status=success_code)

    if _type == 'team/startup':
        Media.objects.create(team_id=current_owner_id, url=cover_youtube_video_url, set_as_cover=True, media_type='vid')
        return Response(data={'status': 'success'}, status=success_code)

    if _type == 'org':
        Media.objects.create(organization_id=current_owner_id, url=cover_youtube_video_url, set_as_cover=True,
                             media_type='vid')
        return Response(data={'status': 'success'}, status=success_code)

    if _type == 'contest':
        Media.objects.create(contest_id=current_owner_id, url=cover_youtube_video_url, set_as_cover=True,
                             media_type='vid')
        return Response(data={'status': 'success'}, status=success_code)

    if _type == 'event':
        Media.objects.create(event_id=current_owner_id, url=cover_youtube_video_url, set_as_cover=True,
                             media_type='vid')
        return Response(data={'status': 'success'}, status=success_code)

    if _type == 'post':
        Media.objects.create(post_id=current_owner_id, url=cover_youtube_video_url, set_as_cover=True, media_type='vid')
        return Response(data={'status': 'success'}, status=success_code)


def middle_data_transfer(value):
    """Transfer value in request to correct data type in python"""
    if value == 'true':
        return True
    elif value == 'false':
        return False
    return value


def data_from_method_post_put_delete(request: Request, *args) -> tuple:
    """
    :param request: request từ client
    :param args: Danh sách các key trong request
    :return tuple: (data1, data2, ...) or (data1,) if only take one key from request
    """

    def get_data():
        for key in args:
            if request.data.get(key) is not None:
                yield middle_data_transfer(request.data.get(key))
            else:
                # Cho phương thức delete
                yield middle_data_transfer(request.query_params.get(key))

    return tuple(get_data())


def data_from_method_get(request: Request, *args) -> tuple:
    """
    :param request: request từ client
    :param args: Danh sách các key trong request
    :return tuple: (data1, data2, ...)
    """

    def get_data():
        for key in args:
            yield middle_data_transfer(request.query_params.get(key))

    return tuple(get_data())


def generate_secret_key(nbyte: int, s_type: str = 'token_hex') -> Type[str]:
    """
    Tạo secret key
    :param nbyte: Số byte của secret key
    :param s_type: token_hex | token_urlsafe
    :return: secret_key
    """
    if s_type == 'token_hex':
        return secrets.token_hex(nbyte)
    elif s_type == 'token_urlsafe':
        return secrets.token_urlsafe(nbyte)


def get_translate(_objects=None, _field=None, _language_id=None):
    if not _objects or not _field:
        return None
    _text = _objects.filter(field=_field, language_id=_language_id)
    return _text.first().text if _text else None


def convert_str_date_datetime(_str_date):
    from datetime import datetime
    return datetime.fromisoformat(_str_date)


def get_host_name(request: Request) -> str:
    try:
        real_ip = request.META['HTTP_X_FORWARDED_FOR']
        reg_ip = real_ip.split(",")[0]
    except:
        try:
            reg_ip = request.META['REMOTE_ADDR']
        except:
            reg_ip = ""
    if (reg_ip == "127.0.0.1"):
        myHost = socket.gethostname()
    else:
        resultHost = socket.gethostbyaddr(reg_ip)
        myHost = resultHost[0]
    return myHost
