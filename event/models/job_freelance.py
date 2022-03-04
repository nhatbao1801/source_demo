from datetime import datetime

from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now

from .contest import Contest
from .team import Team
from .organization import Organization
from .user import User


class JobFreelance(models.Model):
    user = models.ForeignKey(to=User, blank=True, null=True, on_delete=models.PROTECT)
    team = models.ForeignKey(to=Team, blank=True, null=True, on_delete=models.PROTECT)
    organization = models.ForeignKey(to=Organization, blank=True, null=True, on_delete=models.PROTECT)
    contest = models.ForeignKey(to=Contest, blank=True, null=True, on_delete=models.PROTECT)
    title = models.CharField(max_length=255, help_text='Tên dự án')
    slug = models.SlugField(max_length=300)
    description = models.CharField(max_length=3500, help_text="Mô tả công việc")
    budget_min = models.DecimalField(max_digits=40, decimal_places=3, help_text='Ngân sách tối thiểu')
    budget_max = models.DecimalField(max_digits=40, decimal_places=3, help_text='Ngân sách ngân sách tối đa')
    expired_at = models.DateTimeField(help_text='Ngày hết hạn')
    last_modified = models.DateTimeField(help_text='Thời gian sửa đổi lần cuối', blank=True, null=True)

    class Meta:
        db_table = 'hinnox_jobs_freelance'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title) + '-' + str(abs(hash(datetime.now())))
        self.last_modified = now()
        return super().save()

    def get_owner(self):
        if self.team is not None:
            return self.team
        if self.organization is not None:
            return self.organization
        if self.contest is not None:
            return self.contest
