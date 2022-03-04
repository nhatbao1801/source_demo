from django.db import models
from django.utils.translation import gettext_lazy as _


class City(models.Model):
    """City model - Thành phố"""
    name = models.CharField(max_length=100, help_text=_('City name'), verbose_name=_('Name'))
    country = models.ForeignKey(to='main.Country', on_delete=models.CASCADE, verbose_name=_('Country'))

    class Meta:
        db_table = 'hinnox_cities'
        verbose_name = _('City')
        verbose_name_plural = _('Cities')

    def __str__(self):
        return self.name
