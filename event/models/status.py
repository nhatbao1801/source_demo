from django.db import models


class Status(models.Model):
    name = models.CharField(max_length=255, verbose_name='Tên', help_text='Trạng thái tìm kiếm cơ hôi của user')

    class Meta:
        db_table = 'hinnox_status'
        verbose_name = 'trạng thái'
        verbose_name_plural = 'Status - Trạng thái'
