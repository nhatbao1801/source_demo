from django.db import models
from django.utils.translation import gettext_lazy as _


class Area(models.Model):
    """ Area model - Các kỹ năng """
    name = models.CharField(max_length=55, verbose_name=_('Name'), help_text=_('JavaScript, Python, Java, Ruby etc.'))
    types = models.ManyToManyField(to='event.EventType', verbose_name=_('type'), help_text=_('types'), db_table='hinnox_areas_types')

    class Meta:
        db_table = 'hinnox_areas'
        verbose_name = _('Area')
        verbose_name_plural = _('Areas')

    def __str__(self):
        return self.name
