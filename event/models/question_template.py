from django.db import models
from .question_template_type import QuestionTemplateType


class QuestionTemplate(models.Model):
    type = models.ForeignKey(to=QuestionTemplateType, blank=True, null=True, on_delete=models.SET_NULL)
    content = models.CharField(max_length=255, help_text='Nội dung câu hỏi dưới dạng định dạng html')
    description = models.CharField(max_length=255, blank=True, null=True, help_text='Mô tả câu hỏi')
    is_required = models.BooleanField(default=False, help_text='Câu hỏi bắt buộc hay không?')
    limit_answer_length = models.SmallIntegerField(blank=True, null=True, help_text='Giới hạn độ dài câu trả lời')
    show_description = models.BooleanField(default=True, help_text='Hiển thị mô tả dưới câu hỏi hay không')
    required_confirmation = models.BooleanField(default=True, help_text='Yêu cầu xác nhận câu trả lời')

    class Meta:
        db_table = 'hinnox_questions_template'

    def __str__(self):
        return self.content
