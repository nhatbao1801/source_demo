from datetime import datetime

from django.contrib.humanize.templatetags import humanize
from django.db import models
from .user import User
from .team import Team
from .organization import Organization
from .contest import Contest
from .event import Event
from .deal import Deal
from .privacy_setting import PrivacySetting


class Post(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, help_text='User đăng bài')
    team = models.ForeignKey(to=Team, blank=True, null=True, on_delete=models.PROTECT)
    organization = models.ForeignKey(to=Organization, blank=True, null=True, on_delete=models.PROTECT)
    contest = models.ForeignKey(to=Contest, blank=True, null=True, on_delete=models.CASCADE)
    # event = models.ForeignKey(to=Event, blank=True, null=True, on_delete=models.PROTECT)
    deal = models.ForeignKey(to=Deal, blank=True, null=True, on_delete=models.PROTECT)
    privacy_setting = models.ForeignKey(to=PrivacySetting, on_delete=models.PROTECT)
    content = models.TextField(help_text='Nội dung của bài viết')
    date_created = models.DateTimeField(default=datetime.today)

    class Meta:
        db_table = 'hinnox_posts'

    def __str__(self):
        return self.content

    def get_date(self):
        return humanize.naturaltime(self.date_created)
