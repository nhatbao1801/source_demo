from django.db import models


class FundingStage(models.Model):
    name = models.CharField(max_length=50, help_text='Giai đoạn gọi vốn đầu tư')
    code = models.CharField(max_length=50, blank=True, null=True, help_text='Code')

    class Meta:
        db_table = 'hinnox_funding_stages'

    def __str__(self):
        return self.name
