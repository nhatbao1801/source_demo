from django.db import models
from .user import User
from .notification_setting import NotificationSetting


class UserNotificationSetting(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    notification_setting = models.ForeignKey(to=NotificationSetting, on_delete=models.CASCADE)
    state = models.BooleanField(default=False, help_text='Bật/Tắt cài đặt')

    class Meta:
        db_table = 'hinnox_user_notification_settings'
