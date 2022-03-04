from django.db import models
from .deal import Deal
from .organization import Organization


class DealDistribution(models.Model):
    """
    Tổ chức đóng vai trò phân phối các deal
    """
    deal = models.ForeignKey(to=Deal, on_delete=models.CASCADE)
    organization = models.ForeignKey(to=Organization, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)

    class Meta:
        db_table = 'hinnox_deal_distribution'
