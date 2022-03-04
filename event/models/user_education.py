from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from .user import User
from .university import University
from .major import Major
from .degree import Degree


class UserEducation(models.Model):
    university = models.ForeignKey(to=University, blank=True, null=True, on_delete=models.SET_NULL)
    university_name = models.CharField(max_length=512, blank=True, null=True,
                                       help_text=_('require when university id is null'))
    major = models.ForeignKey(to=Major, blank=True, null=True, on_delete=models.SET_NULL)
    degree = models.ForeignKey(to=Degree, blank=True, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    from_date = models.DateTimeField(help_text='Ngày bắt đầu học')
    to_date = models.DateTimeField(help_text='Ngày tốt nghiệp', blank=True, null=True)
    is_currently_studying = models.BooleanField(help_text='Hiện tại đang học hay không?')
    description = models.CharField(max_length=2500, blank=True, null=True, help_text='Chiều dài tối đa của mô tả')
    last_modified = models.DateTimeField(help_text='Thời gian sửa đổi lần cuối', blank=True, null=True)

    class Meta:
        db_table = 'hinnox_users_educations'

    def save(self, *args, **kwargs):
        if self.to_date is None:
            self.is_currently_studying = True
        else:
            self.is_currently_studying = False
        self.last_modified = now()
        return super(UserEducation, self).save()

    def __str__(self):
        if self.university is None:
            return f'{self.user.username}-{self.university_name}' if self.university_name is not None \
                else self.user.username
        return f'{self.user.username}-{self.university.name}'
