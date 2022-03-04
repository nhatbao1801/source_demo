from django.db import models
from django.utils.translation import gettext_lazy as _


class NotificationSetting(models.Model):
    """
    Cài đặt thông báo
    """
    name = models.CharField(max_length=255, verbose_name='Tên cài đặt')
    code = models.CharField(max_length=15, blank=True, null=True, help_text=_('Notification code'))

    class Meta:
        db_table = 'hinnox_notification_settings'
        verbose_name = 'cài đặt thông báo'
        verbose_name_plural = 'NotificationSetting - Cài đặt thông báo'

    def __str__(self):
        return self.name
