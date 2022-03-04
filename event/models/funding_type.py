from django.db import models
from django.utils.translation import gettext_lazy as _


class FundingType(models.Model):
    name = models.CharField(max_length=20, help_text='Kiểu đầu tư(Team, Founder, Prize)')

    class Meta:
        db_table = 'hinnox_funding_types'
        verbose_name = _('kiểu đầu tư')
        verbose_name_plural = _('FundingType - Các kiểu đầu tư')

    def __str__(self):
        return self.name
