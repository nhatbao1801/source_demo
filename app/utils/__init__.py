import logging
import secrets
import socket
from typing import Type

from rest_framework.request import Request

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
