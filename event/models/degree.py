#  Copyright (c) 2020.
#  Team hspaces.net
#  Contributors sang.tanhle, HuynhDH
from django.db import models


class Degree(models.Model):
    name = models.CharField(max_length=255, help_text='Tên bằng cấp')

    class Meta:
        db_table = 'hinnox_degree'

    def __str__(self):
        return self.name
