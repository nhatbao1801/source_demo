from django.db import models
from .team import Team
from .organization import Organization
from .contest import Contest
from .type import Type


class Market(models.Model):
    team = models.ForeignKey(to=Team, blank=True, null=True, on_delete=models.CASCADE)
    organization = models.ForeignKey(to=Organization, blank=True, null=True, on_delete=models.CASCADE)
    contest = models.ForeignKey(to=Contest, blank=True, null=True, on_delete=models.CASCADE)
    type = models.ForeignKey(to=Type, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'hinnox_market'

    def __str__(self):
        return self.type.category.name
