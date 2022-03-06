from django.contrib.humanize.templatetags import humanize
from django.db import models
from django.utils.translation import gettext_lazy as _

from event.models.base import BaseModel


class Comment(BaseModel):
    """Comment model - Bảng lưu lại các bình luận"""
    user = models.ForeignKey(to='main.User', on_delete=models.CASCADE, verbose_name=_('User'), help_text=_('Who comment'))

    post = models.ForeignKey(to='main.Post', blank=True, null=True, on_delete=models.CASCADE, verbose_name=_('Post'))
    kpi = models.ForeignKey(to='main.KPI', blank=True, null=True, on_delete=models.CASCADE, verbose_name=_('KPI'))
    open_innovation = models.ForeignKey(to='main.OpenInnovation', blank=True, null=True, on_delete=models.CASCADE , verbose_name=_('Challenge'))
    course = models.ForeignKey(to='hSchool.Course', blank=True, null=True, on_delete=models.CASCADE, verbose_name=_('Course'))
    course_announcement = models.ForeignKey(to='hSchool.CourseAnnouncement', blank=True, null=True, on_delete=models.CASCADE, verbose_name='Course announcement')
    course_question_answer = models.ForeignKey(to='hSchool.CourseQuestionAnswer', blank=True, null=True, on_delete=models.CASCADE, verbose_name='Course question answer')

    content = models.TextField(verbose_name=_('Content'), help_text=_('Content of comment'))

    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hinnox_comments'
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

    def __str__(self):
        if len(self.content) <= 50:
            return self.content
        return self.content[:50]

    @property
    def get_date(self):
        return humanize.naturaltime(self.date_created)

    @property
    def get_date_created(self):
        return self.date_created.strftime('%H:%M %d/%m/%Y')
