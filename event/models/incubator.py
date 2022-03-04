from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .organization import Organization
from .team import Team


class Incubator(models.Model):
    """
    Vườn ươm các team của các tổ chức
    """
    organization = models.ForeignKey(to=Organization, on_delete=models.PROTECT)
    team = models.ForeignKey(to=Team, on_delete=models.PROTECT)
    is_accepted = models.BooleanField(_('is accepted'), default=False, help_text='Được chấp nhận vào không?')
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now, help_text='Ngày tham gia')
    date_out = models.DateTimeField(_('date out'), blank=True, null=True, help_text='Ngày ra')

    class Meta:
        db_table = 'hinnox_incubators'
