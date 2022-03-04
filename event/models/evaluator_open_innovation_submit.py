from django.db import models
from models.organization import Organization
from models.open_innovation_submit import OpenInnovationSubmit


class EvaluatorOpenInnovationSubmit(models.Model):
    """
    Dữ liệu điểm mà các tổ chức đánh giá dối với một solution được submit
    """
    evaluator = models.ForeignKey(to=Organization, on_delete=models.DO_NOTHING)
    open_innovation_submit = models.ForeignKey(to=OpenInnovationSubmit, on_delete=models.PROTECT)
    score = models.FloatField(help_text='Số điểm')

    class Meta:
        db_table = 'hinnox_evaluators_open_innovation_submits'
