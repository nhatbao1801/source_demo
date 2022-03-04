from django.db import models


class EventCategory(models.Model):
    """
    Hạng mục nhà tài trợ Gold, Silver etc.
    """
    name = models.CharField(max_length=55, verbose_name='Tên', help_text='Tên hạng mục')

    class Meta:
        db_table = 'hinnox_event_categories'
        verbose_name = 'hạng mục nhà tài trợ'
        verbose_name_plural = 'Event category - Hạng mục nhà tài trợ'

    def __str__(self):
        return self.name
