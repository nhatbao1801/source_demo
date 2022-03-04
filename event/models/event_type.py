from django.db import models


class EventType(models.Model):
    name = models.CharField(max_length=50, help_text='Loại hình sự kiện Meeting, Hackathon, Workshop...')

    class Meta:
        db_table = 'hinnox_event_types'

    def __str__(self):
        return self.name
