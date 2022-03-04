from django.db import models
from .timezone import TimeZone
from .language import Language


class Setting(models.Model):
    timezone = models.ForeignKey(to=TimeZone, blank=True, null=True, on_delete=models.SET_NULL)
    language = models.ForeignKey(to=Language, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'hinnox_settings'
