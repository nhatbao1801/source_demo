from django.db import models
from .application import Application
from .team import Team
from .user import User
from .application_question import ApplicationQuestion


class ApplicationQuestionAnswer(models.Model):
    application = models.ForeignKey(to=Application, blank=True, null=True, on_delete=models.SET_NULL)
    team = models.ForeignKey(to=Team, blank=True, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(to=User, blank=True, null=True, on_delete=models.SET_NULL)
    application_question = models.ForeignKey(to=ApplicationQuestion, blank=True, null=True, on_delete=models.SET_NULL)
    answer = models.TextField(help_text='Câu trả lời')

    class Meta:
        db_table = 'hinnox_applications_questions_answers'

    def __str__(self):
        if len(self.answer) > 50:
            return self.answer[:50]
        return self.answer
