from django.db import models

from .event import Event
from .sponsor import Sponsor


class SponsorEvent(models.Model):
    """
    Danh sách các nhà tài trợ cho các sự kiện
    """
    event = models.ForeignKey(to=Event, on_delete=models.CASCADE)
    sponsor = models.ForeignKey(to=Sponsor, on_delete=models.CASCADE)
    event_category = models.ForeignKey(to='main.EventCategory', blank=True, null=True, on_delete=models.CASCADE)
    custom_category_name = models.CharField(max_length=55, help_text='Hạng mục nhà tài trợ tùy chỉnh')

    class Meta:
        db_table = 'hinnox_sponsors_events'
        verbose_name = 'event sponsor'
        verbose_name_plural = 'Event sponsors'

    def __str__(self):
        return f'{self.event.name} -  {self.sponsor.name} - {self.event_category.name}'
