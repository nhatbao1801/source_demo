from django.db import models
from .open_innovation import OpenInnovation
from .application import Application


class EvaluationCriteria(models.Model):
    application = models.ForeignKey(to=Application, blank=True, null=True, on_delete=models.SET_NULL)
    open_innovation = models.ForeignKey(to=OpenInnovation, blank=True, null=True, on_delete=models.CASCADE)
    criteria_content = models.TextField(help_text='Nội dung điều kiện đánh giá')
    maximum_score = models.FloatField(help_text='Điểm số tối đa cho một điều kiện đánh giá')

    class Meta:
        db_table = 'hinnox_evaluations_criteria'

    def __str__(self):
        return self.criteria_content
