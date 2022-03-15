""" from django.db import models
from django.utils.translation import gettext_lazy as _

from .accept_type import AcceptType
from .base import BaseModel
from .contest import Contest
from .job import Job
from .timezone import TimeZone


class Application(BaseModel):
    # contest = models.OneToOneField(to=Contest, blank=True, null=True, on_delete=models.CASCADE)
    # job = models.OneToOneField(to=Job, blank=True, null=True, on_delete=models.CASCADE)
    # job_freelance = models.OneToOneField(to='JobFreelance', blank=True, null=True, on_delete=models.CASCADE)
    # incubator = models.OneToOneField(to='Incubator', blank=True, null=True, on_delete=models.CASCADE)
    # # open_innovation = models.OneToOneField(to='main.OpenInnovation', blank=True, null=True, on_delete=models.PROTECT)
    # event = models.OneToOneField(to='main.Event', blank=True, null=True, on_delete=models.CASCADE)
    # organization = models.OneToOneField(to='main.Organization', blank=True, null=True, on_delete=models.CASCADE)
    accept_type = models.ForeignKey(to=AcceptType, blank=True, null=True, on_delete=models.SET_NULL)
    apply_from = models.DateTimeField(blank=True, null=True, help_text='Thời điểm bắt đầu nộp đơn đăng ký')
    apply_to = models.DateTimeField(blank=True, null=True, help_text='Thời điểm kết thúc nộp đơn đăng ký')
    run_from = models.DateTimeField(blank=True, null=True, help_text='Thời điểm bắt đầu cuộc thi')
    run_to = models.DateTimeField(blank=True, null=True, help_text='Thời điểm kết thúc kết thúc')
    hide_score = models.BooleanField(blank=True, null=True, default=False,
                                     help_text='Có ẩn điểm của user/team tham gia không?')
    timezone = models.ForeignKey(to=TimeZone, blank=True, null=True, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'hinnox_applications'
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'


class ApplicationForm(BaseModel):
    application = models.ForeignKey(to='main.Application', on_delete=models.CASCADE, blank=True, null=True)
    errors = models.TextField(blank=True, null=True, help_text=_('errors of application form'))
    error_schema = models.TextField(blank=True, null=True, help_text=_('errorsSchema of application form'))
    id_schema = models.TextField(blank=True, null=True, help_text=_('idSchema of application form'))
    schema = models.TextField(blank=True, null=True, help_text=_('schema of application form'))
    ui_schema = models.TextField(blank=True, null=True, help_text=_('uiSchema of application form'))
    form_data = models.TextField(blank=True, null=True, help_text=_('form data custom of application form'))
    images = models.JSONField(blank=True, null=True, help_text=_('images of application form'))
    is_used = models.BooleanField(default=True, blank=True, null=True, help_text=_('form is used'))

    class Meta:
        db_table = 'hinnox_application_form'
        verbose_name = 'Application form'
        verbose_name_plural = 'Application forms'


class ApplicationFormAnswer(BaseModel):
    user = models.ForeignKey(to='main.User', on_delete=models.CASCADE, blank=True, null=True)
    team = models.ForeignKey(to='main.Team', on_delete=models.CASCADE, blank=True, null=True)
    organization = models.ForeignKey(to='main.Organization', on_delete=models.CASCADE, blank=True, null=True)
    contest = models.ForeignKey(to='main.Contest', on_delete=models.CASCADE, blank=True, null=True)

    application_form = models.ForeignKey(to='main.ApplicationForm', on_delete=models.CASCADE)
    form_data_answer = models.TextField(blank=True, null=True,
                                        help_text=_('form data answer custom of application form'))

    class Meta:
        db_table = 'hinnox_application_form_answer'
        verbose_name = 'Application form answer'
        verbose_name_plural = 'Application form answers'

    @property
    def get_owner(self):
        if self.user:
            return self.user
        if self.team:
            return self.team
        if self.organization:
            return self.organization
        if self.contest:
            return self.contest
 """