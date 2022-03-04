from django.db import models
from .team import Team
from .organization import Organization
from .contest import Contest
from .funding_stage import FundingStage
from .security_type import SecurityType
from .privacy_setting import PrivacySetting


class FundRaising(models.Model):
    team = models.OneToOneField(to=Team, blank=True, null=True, on_delete=models.PROTECT)
    organization = models.OneToOneField(to=Organization, blank=True, null=True, on_delete=models.PROTECT)
    contest = models.OneToOneField(to=Contest, blank=True, null=True, on_delete=models.CASCADE)
    funding_stage = models.ForeignKey(to=FundingStage, on_delete=models.DO_NOTHING)
    security_type = models.ForeignKey(to=SecurityType, on_delete=models.DO_NOTHING)
    privacy_setting = models.ForeignKey(to=PrivacySetting, blank=True, null=True, on_delete=models.DO_NOTHING)
    target_valuation = models.DecimalField(max_digits=40, decimal_places=3, help_text='Giá trị hiện tại')
    amount_raising = models.DecimalField(max_digits=40, decimal_places=3, help_text='Số tiền gọi vốn')
    closing_date = models.DateTimeField(help_text='Thời gian kết thúc gọi vốn')
    status = models.BooleanField(default=True, help_text='Trạng thái vòng gọi vốn')

    class Meta:
        db_table = 'hinnox_fund_raisings'

    def __str__(self):
        return str(self.closing_date)
