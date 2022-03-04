from django.db import models


class QuestionTemplateType(models.Model):
    name = models.CharField(max_length=50, help_text='Loại mẫu câu hỏi')

    class Meta:
        db_table = 'hinnox_question_template_type'

    def __str__(self):
        return self.name
