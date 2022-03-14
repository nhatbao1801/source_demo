from datetime import datetime

from cloudinary.models import CloudinaryField
from django.db import models
from django.utils.translation import gettext_lazy as _

from models.organization import Organization
from models.base import BaseModel
from models.open_innovation import OpenInnovation
from models.team import Team
from models.user import User
from serializers.document_serializer import DocumentOutSerializer


class OpenInnovationSubmit(BaseModel):
    open_innovation = models.ManyToManyField(to=OpenInnovation, blank=True,
                                             help_text='Một solution apply cho nhiều problem')
    user = models.ForeignKey(to=User, blank=True, null=True, on_delete=models.PROTECT)
    team = models.ForeignKey(to=Team, blank=True, null=True, on_delete=models.PROTECT)
    organization = models.ForeignKey(to=Organization, blank=True, null=True, on_delete=models.PROTECT)

    title = models.CharField(max_length=1000, blank=True, null=True, help_text="Tiêu đề của giải pháp")
    solution = models.TextField(blank=True, null=True, help_text='Giải pháp mà người dùng hoặc nhóm gửi lên')
    area = models.ManyToManyField(to='main.Area', blank=True, help_text='Lĩnh vực chuyên môn')
    category = models.ManyToManyField(to='main.Category', blank=True, help_text='Lĩnh vực áp dụng')
    is_submitted = models.BooleanField(default=False,
                                       help_text='Trạng thái submit hay chưa của nhóm tham gia open innovation')
    is_winner = models.BooleanField(default=False, help_text='Giải pháp giành chiên thắng hay không?')
    is_admin_accept = models.BooleanField(default=None, blank=True, null=True,
                                          help_text='Admin chấp nhận solution này hay chưa?')
    is_posted = models.BooleanField(default=False, help_text='Đã đăng lên hệ thống hay chưa?')
    is_public = models.BooleanField(default=False, help_text='Đã public hay chưa?')
    date_posted = models.DateTimeField(blank=True, null=True, help_text='Ngày đăng')
    date_public = models.DateTimeField(blank=True, null=True, help_text='Ngày public')
    date_winner = models.DateTimeField(blank=True, null=True, help_text='Ngày giải pháp giành chiến thắng')
    date_submit = models.DateTimeField(blank=True, null=True, help_text='Ngày gửi giải pháp')
    date_create = models.DateTimeField(auto_now_add=True, blank=True, null=True, help_text='Ngày tạo')
    users_saved = models.ManyToManyField(to=User, through='main.UserOpenInnovationSubmitSaved',
                                         related_name='my_saved_open_innovation_submits',
                                         through_fields=('open_innovation_submit', 'user'))
    users_interested_in = models.ManyToManyField(to=User, through='main.UserOpenInnovationSubmitInterest',
                                                 related_name='my_interested_open_innovation_submits',
                                                 through_fields=('open_innovation_submit', 'user'))

    type_solution = models.ForeignKey(to='main.ProblemSolutionType', blank=True, null=True, on_delete=models.CASCADE)
    category_solution = models.ForeignKey(to='main.ProblemSolutionCategory', blank=True, null=True,
                                          on_delete=models.CASCADE)
    status = models.ManyToManyField(to='main.OpenInnovationSubmitStatus', blank=True,
                                    help_text=_('Technical condition'), )
    picture = CloudinaryField('image', blank=True, null=True, help_text='File ảnh')
    abstract = models.TextField(help_text='Tóm tắt giải pháp', blank=True, null=True)
    detail = models.TextField(help_text='Chi tiết giải pháp', blank=True, null=True)
    tags = models.CharField(max_length=128, blank=True, null=True, help_text='Keyword giải pháp')

    class Meta:
        db_table = 'hinnox_open_innovation_submits'
        verbose_name = 'open innovation submit'
        verbose_name_plural = _('Open innovation submit')

    def __str__(self):
        return f'{self.title} - #{self.id}'

    def save(self, *args, **kwargs):
        if self.is_posted:
            self.date_posted = datetime.today()
        if self.is_public:
            self.date_public = datetime.today()
        if self.is_winner:
            self.date_winner = datetime.today()
        if self.is_submitted:
            self.date_submit = datetime.today()
        return super(OpenInnovationSubmit, self).save(*args, **kwargs)

    # @property
    # def get_documents(self):
    #     return DocumentOutSerializer(self.document_set.all(), many=True).data

    @property
    def get_picture(self):
        if not self.picture:
            return None
        return self.picture.build_url()


class UserOpenInnovationSubmitSaved(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE,
                             help_text='User saved an open innovation submit')
    open_innovation_submit = models.ForeignKey(to=OpenInnovationSubmit, on_delete=models.CASCADE,
                                               help_text='Open innovation submit which user has saved')
    datetime_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hinnox_user_openinnovation_submit_saved'
        unique_together = ['user', 'open_innovation_submit']


class UserOpenInnovationSubmitInterest(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE,
                             help_text='User saved an open innovation submit')
    open_innovation_submit = models.ForeignKey(to=OpenInnovationSubmit, on_delete=models.CASCADE,
                                               help_text='Open innovation submit which user has interested')
    datetime_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hinnox_user_openinnovation_submit_interested'
        unique_together = ['user', 'open_innovation_submit']


class OpenInnovationSubmitStatus(models.Model):
    name = models.CharField(max_length=100, help_text=_('Name of status'))

    class Meta:
        db_table = 'hinnox_openinnovation_submit_status'
        verbose_name = 'open innovation submit status'
        verbose_name_plural = _('open innovation submit status')

    def __str__(self):
        return self.name
