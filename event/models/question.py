#  Copyright (c) 2021
#  Team hspaces.net
#  Contributors sang.tanhle, HuynhDH

from django.db import models
from django.utils.translation import gettext_lazy as _


class Question(models.Model):
    topic = models.ForeignKey(to='hSchool.Topic', on_delete=models.CASCADE, help_text=_('Topic of the question'))
    type = models.ForeignKey(to='main.QuestionType', null=True, on_delete=models.SET_NULL,
                             help_text=_('Type of the question'))
    title = models.CharField(max_length=3000, help_text=_('Title of the question'))
    datetime_created = models.DateTimeField(help_text=_('Datetime created of topic'), auto_now_add=True)
    last_modified = models.DateTimeField(help_text=_('Last modified datetime'), auto_now=True)

    class Meta:
        db_table = 'hschool_question'
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self):
        return self.title
