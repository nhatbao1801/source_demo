from django.db import models

from .base import BaseModel
from .organization import Organization
from .contest import Contest
from .funding_type import FundingType
from .country import Country
from .region import Region


class Funding(BaseModel):
    organization = models.ForeignKey(to=Organization, blank=True, null=True, on_delete=models.CASCADE)
    contest = models.OneToOneField(to=Contest, blank=True, null=True, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=3500, blank=True, null=True, help_text='Tên của quỹ')
    funding_type = models.ForeignKey(to=FundingType, blank=True, null=True, on_delete=models.DO_NOTHING)
    countries = models.ManyToManyField(to=Country, blank=True, db_table='hinnox_funding_countries')
    regions = models.ManyToManyField(to=Region, blank=True, db_table='hinnox_funding_regions')
    equity = models.FloatField(blank=True, null=True, help_text='Số cổ phần để match với các start up')
    amount = models.DecimalField(blank=True, null=True, max_digits=40, decimal_places=3,
                                 help_text='Số lượng tiền đầu tư')
    number_of_startup_per_month = models.PositiveSmallIntegerField(blank=True, null=True,
                                                                   help_text='Số lượng start up đầu tư / 1 tháng')
    number_of_startup_per_year = models.PositiveSmallIntegerField(blank=True, null=True,
                                                                  help_text='Số lượng start up đầu tư / 1 năm')

    class Meta:
        db_table = 'hinnox_fundings'
