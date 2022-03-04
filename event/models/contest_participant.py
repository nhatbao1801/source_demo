from django.db import models
from .contest import Contest
from .team import Team
from .user import User


class ContestParticipant(models.Model):
    contest = models.ForeignKey(to=Contest, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, blank=True, null=True, on_delete=models.CASCADE)
    team = models.ForeignKey(to=Team, blank=True, null=True, on_delete=models.CASCADE)
    status = models.BooleanField(blank=True, null=True, help_text='Chấp nhận hoặc từ chối')
    score = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'hinnox_contest_participants'
        constraints = [
            models.UniqueConstraint(fields=['user', 'contest'], name='unique_user_contest'),
            models.UniqueConstraint(fields=['team', 'contest'], name='unique_team_contest')
        ]