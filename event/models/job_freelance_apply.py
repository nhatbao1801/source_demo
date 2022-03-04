from django.db import models
from .user import User
from .job_freelance import JobFreelance


class JobFreelanceApply(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.PROTECT)
    job_freelance = models.ForeignKey(to=JobFreelance, on_delete=models.PROTECT)
    bid_comment = models.CharField(max_length=2500, blank=True, null=True, help_text='Lời chào')
    bid = models.DecimalField(max_digits=40, decimal_places=3, help_text='Chào giá')
    number_of_days = models.SmallIntegerField(blank=True, null=True, help_text='Số lượng ngày hoàn thành')
    number_of_hours = models.SmallIntegerField(blank=True, null=True, help_text='Số lượng giờ hoàn thành')
    status = models.BooleanField(help_text='Chấp nhận hoặc không')
    date_applied = models.DateTimeField(help_text='Ngày chào giá')

    class Meta:
        db_table = 'hinnox_jobs_freelance_applies'
