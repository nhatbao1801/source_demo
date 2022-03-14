from django.db import models
from django.utils.timezone import now

from .position import Position
from organization import Organization, City
from .base import BaseModel
from .user import User
from .team import Team
from .role import Role


class UserExperience(BaseModel):
    """
    Kinh nghiệm làm việc của user
    """
    user = models.ForeignKey(to=User, on_delete=models.PROTECT)
    team = models.ForeignKey(to=Team, blank=True, null=True, on_delete=models.PROTECT)
    organization = models.ForeignKey(to=Organization, blank=True, null=True, on_delete=models.PROTECT)
    role = models.ForeignKey(to=Role, blank=True, null=True, on_delete=models.PROTECT)
    position = models.ForeignKey(to=Position, blank=True, null=True, on_delete=models.PROTECT)
    hstartup_position = models.ForeignKey(to='hStartup.HStartupPosition', blank=True, null=True,
                                          on_delete=models.CASCADE)
    job_location = models.ForeignKey(to=City, blank=True, null=True, on_delete=models.SET_NULL)
    job_title = models.CharField(max_length=255, blank=True, null=True, help_text='Tiêu đề công việc')
    name = models.CharField(max_length=255, blank=True, null=True,
                            help_text='Tên công ty đã làm việc hoặc đang làm việc')
    is_confirmed = models.BooleanField(default=True,
                                       help_text='Trạng thái xác nhận công ty có trong hệ thống hay không')
    from_date = models.DateTimeField(help_text='Ngày bắt đầu làm')
    to_date = models.DateTimeField(help_text='Ngày kết thúc', null=True)
    work_schedule = models.CharField(max_length=25, blank=True, null=True, help_text='Chế dộ làm việc full, parttime')
    description = models.CharField(max_length=200, blank=True, null=True, help_text='Mô tả về những việc đã làm')
    is_currently_working = models.BooleanField(help_text='Hiện tại đang làm hay không?')
    last_modified = models.DateTimeField(help_text='Thời gian sửa đổi lần cuối', blank=True, null=True)

    class Meta:
        db_table = 'hinnox_user_experiences'
        verbose_name = 'Kinh nghiệm người dùng'
        verbose_name_plural = 'User Experiences - Kinh nghiệm người dùng'

    def __str__(self):
        return f'{self.user.username} - {self.job_title} - {self.team or self.organization or self.position or self.hstartup_position}'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.team or self.organization:
            self.is_confirmed = True
        else:
            self.is_confirmed = False
        self.last_modified = now()
        return super(UserExperience, self).save()

    def get_working_place(self):
        """
        Xác định nơi làm việc
        :return: [name, id-unique_id, type]
        """
        if self.team:
            return [self.team.name, f'{self.team_id}-{self.team.unique_id}', 'team']
        if self.organization:
            return [self.organization.name, f'{self.organization_id}-{self.organization.unique_id}', 'org']
        return self.name

    def get_position_or_role(self):
        """
        Xác định vị trí, vai trò tại nơi làm việc
        :return: [name, type, id]
        """
        if self.position:
            return [self.position.name, 'position', f'{self.position_id}']
        if self.role:
            return [self.role.name, 'role', f'{self.team_id}']
        return None
