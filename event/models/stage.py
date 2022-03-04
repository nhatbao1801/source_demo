from django.db import models


class Stage(models.Model):
    """
    Các giai doạn đoạn của một startup Ideas, Basic research, technology formulation, applied proof,
    research concept, small-scale prototype, large-scale prototype,prototype system,
    demo system, first comercial system, full comercial system, successful system
    """
    context = models.CharField(max_length=125, verbose_name='Giai đoạn', help_text='Giai đoạn của startup')

    class Meta:
        db_table = 'hinnox_stages'
        verbose_name = 'giai đoạn'
        verbose_name_plural = 'Stage - Giai đoạn của team/startup'

    def __str__(self):
        return self.context
