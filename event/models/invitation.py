from django.db import models

from hSchool.models import Course
from .user import User
from .team import Team
from .organization import Organization
from .contest import Contest
from .event import Event
from .position import Position


class Invitation(models.Model):
    team = models.ForeignKey(to=Team, blank=True, null=True, on_delete=models.PROTECT)
    organization = models.ForeignKey(to=Organization, blank=True, null=True, on_delete=models.PROTECT)
    constest = models.ForeignKey(to=Contest, blank=True, null=True, on_delete=models.PROTECT)
    event = models.ForeignKey(to=Event, blank=True, null=True, on_delete=models.PROTECT)
    course = models.ForeignKey(to=Course, blank=True, null=True, on_delete=models.PROTECT)
    to_user = models.ForeignKey(to=User, on_delete=models.PROTECT, null=True, blank=True)
    position = models.ForeignKey(to=Position, on_delete=models.DO_NOTHING, help_text='Vị trí người được mời vào',
                                 null=True, blank=True)
    role = models.ForeignKey(to='main.Role', blank=True, null=True, on_delete=models.DO_NOTHING)
    hstartup_position = models.ForeignKey(to='hStartup.HStartupPosition', on_delete=models.DO_NOTHING,
                                          help_text='Vị trí người được mời vào hStartup', null=True, blank=True)
    init_message = models.TextField(help_text='Thông điệp lời mời')
    email = models.EmailField(blank=True, null=True, help_text='Email để gửi lời mời')
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    is_accepted = models.BooleanField(default=False, help_text='Lời mời được chấp nhận hay không?')

    class Meta:
        db_table = 'hinnox_invitations'

    def __str__(self):
        return self.init_message
