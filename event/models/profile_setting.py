from django.db import models
from django.utils.translation import gettext_lazy as _

from .user import User
from .team import Team
from .deal import Deal
from .organization import Organization
from .contest import Contest
from .event import Event
from .job import Job


class ProfileSetting(models.Model):
    user = models.OneToOneField(to=User, blank=True, null=True, on_delete=models.CASCADE)
    team = models.OneToOneField(to=Team, blank=True, null=True, on_delete=models.CASCADE)
    deal = models.OneToOneField(to=Deal, blank=True, null=True, on_delete=models.CASCADE)
    organization = models.OneToOneField(to=Organization, blank=True, null=True, on_delete=models.CASCADE)
    contest = models.OneToOneField(to=Contest, blank=True, null=True, on_delete=models.CASCADE)
    event = models.OneToOneField(to=Event, blank=True, null=True, on_delete=models.CASCADE)
    job = models.OneToOneField(to=Job, blank=True, null=True, on_delete=models.CASCADE)

    visibility = models.BooleanField(help_text='Cho phép profile hiển thị hay không?')
    is_deleted = models.BooleanField(default=False, help_text='Trạng thái xóa của profile')
    show_team = models.BooleanField(default=True, help_text='Hiển thị team trên trang của trang của tổ chức')

    class Language(models.TextChoices):
        VN = 'vi', _('Vietnamese')
        EN = 'en-us', _('English')

    language = models.CharField(max_length=5, choices=Language.choices, help_text='Ngôn ngữ', blank=True, null=True)

    class Meta:
        db_table = 'hinnox_profile_settings'
        verbose_name = _('thiết lập')
        verbose_name_plural = _('ProfileSettings - Thiết lập tài khoản')

    def __str__(self):
        return str(self.id)
