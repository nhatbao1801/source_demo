from django.db import models
from django.utils.translation import gettext_lazy as _


class Region(models.Model):
    """Region model -  Vùng"""
    name = models.CharField(max_length=72, verbose_name=_('Name'), help_text=_('Region name'))

    class Meta:
        db_table = 'hinnox_regions'
        verbose_name = _('Region')
        verbose_name_plural = _('Regions')

    def __str__(self):
        return self.name
