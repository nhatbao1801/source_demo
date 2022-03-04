from django.db import models
from django.utils.translation import gettext_lazy as _

from .deal import Deal
from .user import User
from .post import Post
from .kpi import KPI


class Heat(models.Model):
    user = models.ForeignKey(to=User, blank=True, null=True, on_delete=models.CASCADE)
    post = models.ForeignKey(to=Post, blank=True, null=True, on_delete=models.CASCADE)
    kpi = models.ForeignKey(to=KPI, blank=True, null=True, on_delete=models.CASCADE)
    deal = models.ForeignKey(to=Deal, blank=True, null=True, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(help_text=_('Last time modification'), auto_now=True, blank=True,
                                         null=True)
    state = models.BooleanField(default=True)

    class Meta:
        db_table = 'hinnox_heats'
        unique_together = [
            ['user', 'post'],
            ['user', 'kpi'],
            ['user', 'deal'],
        ]

    def __str__(self):
        return f'{self.user.username}-{self.last_modified}'

    @property
    def target_heat(self):
        if self.post:
            return self.post.content[:100]
        if self.kpi:
            return self.kpi.id
        if self.deal:
            return self.deal.title[:200]
