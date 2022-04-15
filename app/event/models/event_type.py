from django.db import models
from event.models.base_model import BaseModel


class EventType(BaseModel):
    name = models.CharField(max_length=255, help_text='Privacy name')
    code = models.CharField(max_length=255, help_text='Privacy code')


    class Meta:
        db_table = 'event_type'
        verbose_name = 'event_type'
        verbose_name_plural = 'event_type'

    def __str__(self):
        return self.name