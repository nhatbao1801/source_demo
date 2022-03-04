from django.db import models
from .user import User
from .team import Team
from .organization import Organization
from .contest import Contest
from .event import Event


class ExternalLink(models.Model):
    user = models.ForeignKey(to=User, blank=True, null=True, on_delete=models.CASCADE)
    team = models.ForeignKey(to=Team, blank=True, null=True, on_delete=models.CASCADE)
    organization = models.ForeignKey(to=Organization, blank=True, null=True, on_delete=models.CASCADE)
    contest = models.ForeignKey(to=Contest, blank=True, null=True, on_delete=models.CASCADE)
    event = models.ForeignKey(to=Event, blank=True, null=True, on_delete=models.CASCADE)

    class Site(models.TextChoices):
        FACEBOOK = 'fb', 'Facebook'
        TWITTER = 'tw', 'Twitter'
        LINKEDIN = 'lkln', 'Linkedln'
        OTHERS = 'other', 'other'

    site_origin = models.CharField(max_length=10, choices=Site.choices, help_text='Nguồn gốc của link ví dụ Facebook')
    url = models.URLField(blank=True, null=True, help_text='Nội dung url')

    class Meta:
        db_table = 'hinnox_external_links'

    def __str__(self):
        return self.url
