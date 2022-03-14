from datetime import datetime

from django.contrib.humanize.templatetags import humanize
from django.db import models

from models.course import Course
from models.user import User


class CourseAnnouncement(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, help_text='User thông báo')
    course = models.ForeignKey(to=Course, blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=2000, help_text='Tiêu đề của Announcements')
    content = models.TextField(help_text='Nội dung của Announcements')
    date_created = models.DateTimeField(default=datetime.today)
    public = models.BooleanField(default=False, blank=True, null=True, help_text='Public announcement')

    class Meta:
        db_table = 'hschool_course_announcement'

    def __str__(self):
        return self.title

    def get_date(self):
        return humanize.naturaltime(self.date_created)
