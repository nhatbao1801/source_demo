from django.db import models


class AcceptType(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'hinnox_accept_types'
