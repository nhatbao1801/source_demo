from datetime import datetime

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.text import slugify
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Meta:
        db_table = 'hinnox_users'
        verbose_name = 'người dùng'
        verbose_name_plural = 'User - Người dùng'