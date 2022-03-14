from django.db import models


class PrivacySetting(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name='Tên cài đặt',
                            help_text='Tên cài đặt bảo mật '
                                      'public, insider(team, investor, advisor), '
                                      'investor only, team only')
    code = models.CharField(max_length=20,
                            verbose_name='Mã quyền riêng tư',
                            help_text='Mã <= 20 ký tự đại diện quyền riêng tư',
                            unique=True)

    class Meta:
        db_table = 'hinnox_privacy_settings'
        verbose_name = 'cài đặt riêng tư'
        verbose_name_plural = 'PrivacySetting - Cài đặt riêng tư'

    def __str__(self):
        return self.name
