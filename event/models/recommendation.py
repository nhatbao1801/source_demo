from django.db import models

from . import Event
from .user import User
from .team import Team
from .organization import Organization
from .contest import Contest


class Recommendation(models.Model):
    user_ask_for = models.ForeignKey(to=User, related_name='asked_for_recommendation_set', blank=True, null=True,
                                     on_delete=models.PROTECT)
    team_ask_for = models.ForeignKey(to=Team, blank=True, null=True, on_delete=models.PROTECT)
    organization_ask_for = models.ForeignKey(to=Organization, blank=True, null=True, on_delete=models.PROTECT)
    contest_ask_for = models.ForeignKey(to=Contest, blank=True, null=True, on_delete=models.PROTECT)
    event_ask_for = models.ForeignKey(to=Event, blank=True, null=True, on_delete=models.PROTECT)
    user_being_ask = models.ForeignKey(to=User, blank=True, null=True, related_name='was_asked_for_recommendation_set', on_delete=models.PROTECT)

    email = models.EmailField(blank=True, null=True, help_text='Email giúp hệ thống liên hệ với người được yêu cầu giới thiệu')
    name = models.CharField(max_length=50, blank=True, null=True, help_text='Tên của người được yêu cầu giới thiệu')
    is_confirmed = models.BooleanField(max_length=50, default=False, help_text='Xác định trạng thái lời đề nghị')
    reply = models.CharField(max_length=250, blank=True, null=True, help_text='Lời giới thiệu từ người được đề nghị')

    class Meta:
        db_table = 'hinnox_recommendations'
        unique_together = [
            ['user_ask_for', 'user_being_ask'],
            ['team_ask_for', 'user_being_ask'],
            ['organization_ask_for', 'user_being_ask'],
            ['contest_ask_for', 'user_being_ask'],
            ['event_ask_for', 'user_being_ask'],
            ['user_ask_for', 'email'],
            ['team_ask_for', 'email'],
            ['organization_ask_for', 'email'],
            ['contest_ask_for', 'email'],
            ['event_ask_for', 'email'],
        ]

    def __str__(self):
        return str(self.id)
