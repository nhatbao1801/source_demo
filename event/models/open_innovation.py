from datetime import datetime

import cloudinary.api
from cloudinary.models import CloudinaryField
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from rest_framework.reverse import reverse

from .base import BaseModel
from .organization import Organization


class OpenInnovation(BaseModel):
    user = models.ForeignKey(to='main.User', on_delete=models.PROTECT, blank=True, null=True)
    team = models.ForeignKey(to='main.Team', on_delete=models.PROTECT, blank=True, null=True)
    organization = models.ForeignKey(to=Organization, on_delete=models.PROTECT, blank=True, null=True)
    # guaranteed_organization = models.ForeignKey(to=Organization, related_name='was_guaranteed_by_us', blank=True,
    #                                             null=True, on_delete=models.PROTECT, help_text='Tổ chức trung gian')
    name = models.CharField(max_length=10000, blank=True, null=True, help_text='Tên thách thức')
    deadline = models.DateTimeField(help_text='Ngày kết thúc open innovation')
    tags = models.CharField(max_length=128, blank=True, null=True, help_text='Tags giúp tìm kiếm open innovation')
    abstract = models.TextField(help_text='Yêu cầu chính của open innovation')
    overview = models.TextField(help_text='Tổng quan về open innovation')
    detail = models.TextField(help_text='Chi tiết về open innovation')
    picture = CloudinaryField('image', blank=True, null=True, help_text='File ảnh')
    picture_url = models.URLField(blank=True, null=True, help_text='URL của ảnh đại diện của open innovation')
    area = models.ManyToManyField(to='main.Area', blank=True, help_text='Lĩnh vực chuyên môn')
    category = models.ManyToManyField(to='main.Category', blank=True, help_text='Lĩnh vực áp dụng')
    budget = models.DecimalField(max_digits=40, decimal_places=2, blank=True, null=True,
                                 help_text='Ngân sách cho challenge')
    users_saved = models.ManyToManyField(to='main.User', through='main.UserOpenInnovationSaved',
                                         related_name='my_saved_openinnovations',
                                         through_fields=('open_innovation', 'user'))
    users_interested_in = models.ManyToManyField(to='main.User', through='main.UserOpenInnovationInterest',
                                                 related_name='my_interested_openinnovations',
                                                 through_fields=('open_innovation', 'user'))
    is_through_intermediaries = models.BooleanField(default=False,
                                                    help_text="có thông qua tổ chức trung gian hay không?")

    type_challenge = models.ForeignKey(to='main.ProblemSolutionType', blank=True, null=True, on_delete=models.CASCADE)
    category_challenge = models.ForeignKey(to='main.ProblemSolutionCategory', blank=True, null=True,
                                           on_delete=models.CASCADE)

    class StatusChoice(models.TextChoices):
        OPEN = 'OPEN', 'Open'
        CLOSED = 'CLOSED', 'Closed'
        UNDER_EVALUATION = 'UNEVA', 'Under Evaluation'

    status = models.CharField(max_length=6, choices=StatusChoice.choices, help_text='Trạng thái của open innovation')
    term_of_use = models.TextField(help_text='Điều khoản sử dụng open innovation')
    is_anonymity = models.BooleanField(default=False, help_text="Có ẩn danh tính hay không?")
    is_posted = models.BooleanField(default=False, help_text="Đã đăng hay chưa?")
    posted_date = models.DateTimeField(blank=True, null=True, help_text='Ngày mở open innovation')
    date_create = models.DateTimeField(auto_now_add=True, blank=True, null=True, help_text="Ngày tạo open innovation")

    def __str__(self):
        return f'{self.name} - #{self.id}'

    def delete(self, *args, **kwargs):
        """Delete remote picture before delete"""
        if self.picture:
            cloudinary.api.delete_resources(self.picture.public_id)
        return super(OpenInnovation, self).delete()

    def save(self, *args, **kwargs):
        if self.is_posted:
            self.posted_date = datetime.today()
        return super(OpenInnovation, self).save(*args, **kwargs)

    class Meta:
        db_table = 'hinnox_open_innovation'
        verbose_name = 'open innovation'
        verbose_name_plural = _("Open innovation")

    @property
    def get_absolute_url(self):
        return reverse('challenge:detail', kwargs={'pk': self.id})

    @property
    def get_api_url(self):
        return reverse('challenge:challenge-detail', kwargs={'pk': self.id})

    def get_picture_url(self):
        return self.picture.build_url() if self.picture else ''


class IntermediateOrganizationOpenInnovation(BaseModel):
    organization = models.ForeignKey(to=Organization, on_delete=models.CASCADE, help_text="Organization trung gian")
    open_innovation = models.ForeignKey(to=OpenInnovation, on_delete=models.CASCADE)
    init_message = models.TextField(blank=True, null=True, help_text='Thông điệp lời mời')
    reply = models.CharField(max_length=300, blank=True, null=True, help_text='Phản hồi của tổ chức trung gian')
    is_accepted = models.BooleanField(blank=True, null=True, help_text="Tổ chức trung gian đã chấp nhận hay chưa?")
    status_process = models.ForeignKey(to='main.OpenInnovationStatus', blank=True, null=True, on_delete=models.CASCADE,
                                       help_text="Các trạng thái tiến trình xử lý của agent đối với challenge")
    date_created = models.DateTimeField(auto_now_add=True, help_text="Ngày tổ chức trung gian nhận open innovation")
    date_accepted = models.DateTimeField(blank=True, null=True, help_text="Ngày open innovation được chấp nhận", )

    class Meta:
        db_table = 'hinnox_intermediate_organization_open_innovation'
        verbose_name = 'hinnox intermediate organization open innovation'
        verbose_name_plural = _("Intermediate organization open innovation")

    # def __str__(self):
    #     return f'{self.open_innovation} - {self.status_process} - #{self.id}'

    def save(self, *args, **kwargs):
        if self.is_accepted:
            self.date_accepted = datetime.today()
        if self.status_process:
            status_process = OpenInnovationStatus.objects.get(pk=self.status_process.id)
            if status_process.code == 'PENDING':
                self.is_accepted = None
            elif status_process.code == 'ACCEPTED':
                self.is_accepted = True
            elif status_process.code == 'REJECTED':
                self.is_accepted = False
        return super(IntermediateOrganizationOpenInnovation, self).save(*args, **kwargs)


class OpenInnovationStatus(models.Model):
    code = models.CharField(max_length=100, help_text=_('Code of status'))
    name = models.CharField(max_length=100, help_text=_('Name of status'))

    class Meta:
        db_table = 'hinnox_openinnovation_status'
        verbose_name = 'open innovation status'
        verbose_name_plural = _('open innovation status')

    def __str__(self):
        return self.name


class ProblemOpenInnovation(BaseModel):
    parent = models.ForeignKey(to=OpenInnovation, related_name='parent_of_problem', on_delete=models.PROTECT,
                               blank=True, null=True)
    agent = models.ForeignKey(to='main.Organization', on_delete=models.PROTECT, blank=True, null=True)
    post = models.ForeignKey(to=OpenInnovation, related_name='related_current_problem', on_delete=models.PROTECT,
                             help_text="Bài đăng challenge")
    is_posted = models.BooleanField(default=False, help_text="Trạng thái của open innovation")
    date_posted = models.DateTimeField(blank=True, null=True, help_text="Ngày open innovation được đăng")
    date_created = models.DateTimeField(auto_now_add=True, help_text="Ngày tạo")

    def save(self, *args, **kwargs):
        if self.is_posted:
            self.date_posted = datetime.today()
        return super(ProblemOpenInnovation, self).save(*args, **kwargs)

    class Meta:
        db_table = 'hinnox_problem_open_innovation'
        verbose_name = 'problem open innovation'
        verbose_name_plural = _('problem open innovation')

        constraints = [
            models.UniqueConstraint(fields=['post'], name='unique_challenge')
        ]
