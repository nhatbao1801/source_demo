from django.db import models
from .user import User
from .team import Team
from .organization import Organization
from .contest import Contest
from .event import Event


class Following(models.Model):
    from_user = models.ForeignKey(to=User, related_name='following_others', on_delete=models.PROTECT,
                                  help_text='Người theo dõi')
    to_user = models.ForeignKey(to=User, related_name='followed_by_others', blank=True, null=True,
                                on_delete=models.CASCADE,
                                help_text='Người được theo dõi')
    to_team = models.ForeignKey(to=Team, blank=True, null=True, on_delete=models.CASCADE,
                                help_text='Team được theo dõi')
    to_organization = models.ForeignKey(to=Organization, blank=True, null=True, on_delete=models.CASCADE,
                                        help_text='Tổ chức được theo dõi')
    to_contest = models.ForeignKey(to=Contest, blank=True, null=True, on_delete=models.CASCADE,
                                   help_text='Cuộc thi được theo dõi')
    to_event = models.ForeignKey(to=Event, blank=True, null=True, on_delete=models.CASCADE,
                                 help_text='Sự kiện được theo dõi')
    date_following = models.DateTimeField(auto_now_add=True, help_text='Ngày bắt đầu theo dõi')
    is_following = models.BooleanField(default=True, help_text='user hiện có đang theo dõi đối tượng khác không')

    class Meta:
        db_table = 'hinnox_followings'
        unique_together = [
            ['from_user', 'to_user'],
            ['from_user', 'to_team'],
            ['from_user', 'to_organization'],
            ['from_user', 'to_contest'],
            ['from_user', 'to_event'],
        ]

    def __str__(self):
        if self.to_user is not None:
            return self.to_user.username
        if self.to_team is not None:
            return self.to_team.name
        if self.to_event is not None:
            return self.to_event.name
        if self.to_contest is not None:
            return self.to_contest.title
        if self.to_organization is not None:
            return self.to_organization.name
