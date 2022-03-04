from django.contrib.humanize.templatetags import humanize
from django.db import models
from django.utils.translation import gettext_lazy as _


class Reply(models.Model):
    """Reply model"""
    comment = models.ForeignKey(to='main.Comment', on_delete=models.CASCADE, verbose_name=_('Comment'), help_text=_('Comment'))
    user = models.ForeignKey(to='main.User', on_delete=models.CASCADE, verbose_name=_('User'), help_text=_('Who reply'))
    content = models.TextField(verbose_name=_('Content'), help_text=_('Content of reply'))
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hinnox_replies'
        verbose_name = _('Reply')
        verbose_name_plural = _('Replies')

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
