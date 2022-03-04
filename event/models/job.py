from datetime import datetime

from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now

from .base import BaseModel
from .team import Team
from .organization import Organization
from .position import Position
from .city import City
from .country import Country


class Job(BaseModel):
    parent = models.ForeignKey(to='main.Job', blank=True, null=True, on_delete=models.DO_NOTHING,
                               help_text='Job parent')
    category = models.ForeignKey(to='main.Category', blank=True, null=True, on_delete=models.DO_NOTHING, help_text='Category job')
    team = models.ForeignKey(to=Team, blank=True, null=True, on_delete=models.CASCADE, help_text='Owner job')
    organization = models.ForeignKey(to=Organization, blank=True, null=True, on_delete=models.CASCADE,
                                     help_text='Owner job')
    position = models.ForeignKey(to=Position, on_delete=models.DO_NOTHING, help_text='Position')
    city = models.ForeignKey(to=City, on_delete=models.DO_NOTHING, help_text='City')
    country = models.ForeignKey(to=Country, blank=True, null=True, on_delete=models.DO_NOTHING, help_text='Country')
    skill = models.ManyToManyField(to='main.Area', related_name='skills_job', help_text='Skills job', blank=True)
    job_favorite = models.ManyToManyField(to='main.User', related_name='user_favorite', help_text='User favorite', blank=True)
    title = models.CharField(max_length=255, help_text='Title')
    slug = models.SlugField(max_length=300, help_text='Slug', blank=True, null=True)
    email_contact_to = models.EmailField(help_text='Email contact', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True, help_text='Phone number contact')
    description = models.TextField(help_text='Description', blank=True, null=True)
    requirement = models.TextField(help_text='Job requirement', blank=True, null=True)
    benefit = models.TextField(help_text='Benefit job', blank=True, null=True)
    expired_at = models.DateTimeField(help_text='Expiration date', blank=True, null=True)
    open_number = models.SmallIntegerField(blank=True, null=True, help_text='Opens number')
    salary_min = models.DecimalField(max_digits=40, decimal_places=3, help_text='Min salary', blank=True, null=True)
    salary_max = models.DecimalField(max_digits=40, decimal_places=3, help_text='Max salary', blank=True, null=True)
    pay_equity_min = models.FloatField(blank=True, null=True, help_text='Pay equity min')
    pay_equity_max = models.FloatField(blank=True, null=True, help_text='Pay equity max')

    class WorkScheduleChoices(models.TextChoices):
        PART_TIME = 'PART_TIME', 'PT'
        FULL_TIME = 'FULL_TIME', 'FT'
        REMOTE = 'REMOTE', 'RM'
        TEMPORARY = 'TEMPORARY', 'TE'
    work_schedule = models.CharField(max_length=9, blank=True, null=True, choices=WorkScheduleChoices.choices,
                                     help_text='Work schedule(Part time, Full time, Remote, Temporary')

    class PaymentChoices(models.TextChoices):
        MONTH = 'MONTH', 'MO'
        YEAR = 'YEAR', 'YE'

    form_of_payment = models.CharField(max_length=5, blank=True, null=True, choices=PaymentChoices.choices,
                                       help_text='Form of payment(Month, Year')

    is_negotiable_salary = models.BooleanField(default=False, help_text='Is negotiable salary?')
    is_archived = models.BooleanField(default=False, help_text='Is archived?')

    class Meta:
        db_table = 'hinnox_jobs'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title) + '-' + str(abs(hash(datetime.now())))
        self.last_modified = now()
        return super().save()

    @property
    def is_agents_support(self):
        return True if self.jobagent_set.all() else False

    @property
    def get_owner(self):
        if self.team is not None:
            return self.team
        if self.organization is not None:
            return self.organization
