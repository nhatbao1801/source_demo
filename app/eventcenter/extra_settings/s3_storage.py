#  Copyright (c) 2020
from abc import ABC

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class PublicMediaStorage(S3Boto3Storage, ABC):
    location = settings.AWS_PUBLIC_MEDIA_LOCATION
    file_override = False


class PrivateMediaStorage(S3Boto3Storage, ABC):
    location = settings.AWS_PRIVATE_MEDIA_LOCATION
    default_acl = 'private'
    file_override = False
    custom_domain = False
