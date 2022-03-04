from django.db import models
from django.utils.translation import gettext_lazy as _


class ProblemSolutionCategory(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'hinnox_problem_solution_categories'
        verbose_name = 'Problem solution category'
        verbose_name_plural = _('Problem solution category')

    def __str__(self):
        return self.name
