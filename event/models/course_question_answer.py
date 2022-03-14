from datetime import datetime

from django.contrib.humanize.templatetags import humanize
from django.db import models

from models.module_lesson import ModuleLesson
from models.user import User


class CourseQuestionAnswer(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, help_text='User đăng bài')
    module_lesson = models.ForeignKey(to=ModuleLesson, blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=2000, help_text='Tiêu đề của Q&A')
    content = models.TextField(help_text='Nội dung của Q&A')
    date_created = models.DateTimeField(default=datetime.today)

    class Meta:
        db_table = 'hschool_course_question_answer'

    def __str__(self):
        return self.title

    def get_date(self):
        return humanize.naturaltime(self.date_created)
