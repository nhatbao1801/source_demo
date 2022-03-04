from datetime import datetime

from django.db import models
from .team import Team
from .organization import Organization
from .contest import Contest
from .event import Event
from .privacy_setting import PrivacySetting


class KPI(models.Model):
    team = models.ForeignKey(to=Team, blank=True, null=True, on_delete=models.PROTECT)
    organization = models.ForeignKey(to=Organization, blank=True, null=True, on_delete=models.PROTECT)
    contest = models.ForeignKey(to=Contest, blank=True, null=True, on_delete=models.PROTECT)
    event = models.ForeignKey(to=Event, blank=True, null=True, on_delete=models.PROTECT)
    private_setting = models.ForeignKey(to=PrivacySetting, blank=True, null=True, on_delete=models.SET_NULL)
    revenue = models.DecimalField(max_digits=20, decimal_places=3, help_text='Lợi nhuận')
    num_customer = models.IntegerField(help_text='Số lượng khách hàng mỗi tháng')
    amount_raised = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3,
                                        help_text='Số tiền được gọi vốn được')
    number_of_employee = models.SmallIntegerField(blank=True, null=True, help_text='Số lượng nhân viên')
    total_funding = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3,
                                        help_text='Số tiền đầu tư')
    cash_in_bank = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3,
                                       help_text='Số tiền hiện tại')
    date_created = models.DateTimeField(default=datetime.today, help_text='Ngày tạo hoặc chỉnh sửa')

    class Meta:
        db_table = 'hinnox_kpis'
