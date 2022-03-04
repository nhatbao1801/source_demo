from django.db import models


class QuestionType(models.Model):
    code = models.CharField(max_length=255, blank=True, null=True, help_text='Code loại câu hỏi')
    name = models.CharField(max_length=255, blank=True, null=True, help_text='Tên loại câu hỏi')

    class Meta:
        db_table = 'hinnox_question_type'

    def __str__(self):
        return self.name
