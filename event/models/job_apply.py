from django.db import models

from .base import BaseModel
from .job import Job
from .user import User


class JobApply(BaseModel):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, help_text='User')
    user_cv = models.ForeignKey(to='main.UserCV', blank=True, null=True, on_delete=models.SET_NULL,
                                help_text='Curriculum Vitae User')
    job = models.ForeignKey(to=Job, blank=True, null=True, on_delete=models.SET_NULL, help_text='Job')
    message = models.TextField(blank=True, null=True, help_text='Message')
    is_accept = models.BooleanField(blank=True, null=True, help_text='Is accepted')

    class Meta:
        db_table = 'hinnox_jobs_applies'
        verbose_name = 'Job Apply'
        verbose_name_plural = 'Jobs Applies'

    def __str__(self):
        return f'{self.user} - {self.job} - {self.user_cv}'
