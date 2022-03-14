from django.contrib.humanize.templatetags import humanize
from django.db import models
from django.utils.translation import gettext_lazy as _

from event.models.base import BaseModel


class Comment(BaseModel):
    """Comment model - Bảng lưu lại các bình luận"""
    user = models.ForeignKey(to='event.User', on_delete=models.CASCADE, verbose_name=_('User'), help_text=_('Who comment'))

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
