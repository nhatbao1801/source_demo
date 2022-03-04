from django.db import models
from django.utils.translation import gettext_lazy as _


class Country(models.Model):
    """Country model - Quốc gia"""
    name = models.CharField(max_length=50, help_text=_('Name'), verbose_name=_('Country name'))
    region = models.ForeignKey(to='main.Region', on_delete=models.CASCADE, verbose_name=_('Region'))

    class Meta:
        db_table = 'hinnox_countries'
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')

    def __str__(self):
        return self.name
