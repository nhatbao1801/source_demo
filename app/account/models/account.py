import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class RefAccount(AbstractUser):
    id = models.TextField(primary_key=True, default=uuid.uuid4().hex)
    full_name = models.CharField(max_length=255, blank=True, null=True, help_text='Full name')
    username = models.CharField(
        ('username'),
        max_length=150,
        unique=True,
        help_text=('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': ("A user with that username already exists."),
        },
    )
    user_id = models.CharField(
        max_length=24,
        blank=True,
        null=True,
        help_text='Id user liên kết với service API')
    email = models.EmailField(
        'email address',
        unique=True,
        help_text='Địa chỉ email')

    class Meta:
        db_table = 'event_ref_account'
        verbose_name = 'event Reference Account'
        verbose_name_plural = 'event  Reference Accounts'

    def __str__(self):
        return self.username