from django.db import models
from django.utils.translation import gettext_lazy as _


class SolutionReport(models.Model):
    organization = models.ForeignKey(to='main.Organization', on_delete=models.CASCADE)
    open_innovation = models.ForeignKey(to='main.OpenInnovation', on_delete=models.CASCADE)
    report = models.TextField(blank=True, null=True, help_text=_('Report from organization'))

    class Meta:
        verbose_name = _('Solution report')
        verbose_name_plural = _('Solution report')
        db_table = 'hinnox_solution_report'

    def __str__(self):
        return f'{self.organization} - {self.report}'
