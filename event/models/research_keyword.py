from django.db import models
from .idea import Idea
from .organization import Organization


class ResearchKeyword(models.Model):
    """
    Các từ khóa giúp match các team và và các tổ chức
    """
    idea = models.ForeignKey(to=Idea, blank=True, null=True, on_delete=models.CASCADE)
    organization = models.ForeignKey(to=Organization, blank=True, null=True, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=255, help_text='Từ khóa')

    class Meta:
        db_table = 'hinnox_research_keywords'
