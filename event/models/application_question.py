from django.db import models
from .question_template import QuestionTemplate
from .application import Application
from .question_type import QuestionType


class ApplicationQuestion(models.Model):
    question_type = models.ForeignKey(to=QuestionType, blank=True, null=True, on_delete=models.CASCADE)
    question_template = models.ForeignKey(to=QuestionTemplate, blank=True, null=True, on_delete=models.CASCADE)
    application = models.ForeignKey(to=Application, on_delete=models.PROTECT)
    content = models.CharField(max_length=255, blank=True, null=True, help_text='Nội dung câu hỏi dưới dạng định dạng html')
    description = models.CharField(max_length=255, blank=True, null=True, help_text='Mô tả câu hỏi')
    is_required = models.BooleanField(default=False, blank=True, null=True, help_text='Câu hỏi bắt buộc hay không?')
    limit_answer_length = models.SmallIntegerField(blank=True, null=True, help_text='Giới hạn độ dài câu trả lời')
    show_description = models.BooleanField(default=True, blank=True, null=True, help_text='Hiển thị mô tả dưới câu hỏi hay không')
    required_confirmation = models.BooleanField(default=True, blank=True, null=True, help_text='Yêu cầu xác nhận câu trả lời')
    is_hidden = models.BooleanField(default=False, help_text='Ẩn câu hỏi')
    order_position = models.SmallIntegerField(blank=True, null=True, help_text='Để sắp xếp thứ tự câu hỏi')

    class Meta:
        db_table = 'hinnox_applications_questions'

    def __str__(self):
        if self.content is None:
            return self.question_template
        return self.content
