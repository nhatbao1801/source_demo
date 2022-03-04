from django.db import models
from django.utils.translation import gettext_lazy as _


class ProblemSolutionType(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'hinnox_problem_solution_types'
        verbose_name = 'Problem solution types'
        verbose_name_plural = _('Problem solution types')

    def __str__(self):
        return self.name
