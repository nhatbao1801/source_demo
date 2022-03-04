#  Copyright (c) 2020.
#  Team hspaces.net
#  Contributors sang.tanhle, HuynhDH
from django.db import models


class ReportType(models.Model):
    name = models.CharField(max_length=512, help_text='Tên loại báo cáo')
    level = models.SmallIntegerField(help_text='Mức độ báo cáo')

    class Meta:
        db_table = 'hinnox_report_type'
        verbose_name = 'loại báo cáo'
        verbose_name_plural = 'ReportType - Loại báo cáo'

    def __str__(self):
        return self.name
