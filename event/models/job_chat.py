from django.db import models

from .job_freelance import JobFreelance
from .user import User
from .job import Job


class JobChat(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.PROTECT)
    job = models.ForeignKey(to=Job, blank=True, null=True, on_delete=models.PROTECT)
    job_freelance = models.ForeignKey(to=JobFreelance, blank=True, null=True, on_delete=models.PROTECT)
    content = models.CharField(max_length=1000, help_text='Nội dung tin nhắn')
    date_created = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False, help_text='Đã xem hay chưa')

    class Meta:
        db_table = 'hinnox_job_chats'

    def __str__(self):
        return self.content
