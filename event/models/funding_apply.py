from django.db import models
from django.utils.timezone import now

from models.base import BaseModel


class FundingApply(BaseModel):
    funding = models.ForeignKey(to='main.Funding', on_delete=models.CASCADE, help_text='Qũy đi đầu tư')
    contest = models.ForeignKey(to='main.Contest', blank=True, null=True, on_delete=models.SET_NULL,
                                help_text='Cuộc thi được đầu tư')
    status = models.BooleanField(blank=True, null=True, help_text='Đã chấp nhận đầu tư hay chưa')
    date_accepted = models.DateTimeField(blank=True, null=True, help_text='Thời gian chấp nhận đầu tư')

    class Meta:
        db_table = 'hinnox_funds_applies'
        verbose_name = 'Funding Apply'
        verbose_name_plural = 'Funding Applies'
        constraints = [
            models.UniqueConstraint(fields=['contest', 'funding'], name='unique_contest_funding')
        ]

    def __str__(self):
        return self.funding.name

    def save(self, *args, **kwargs):
        if self.status:
            self.date_accepted = now()
        return super(FundingApply, self).save()
