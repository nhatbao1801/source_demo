from django.db import models
from .team import Team
from .area import Area
from models.privacy_setting import PrivacySetting


class Idea(models.Model):
    team = models.ForeignKey(to=Team, on_delete=models.CASCADE)
    title = models.CharField(max_length=512)
    describe = models.TextField(help_text='Mô tả')
    technologies = models.ManyToManyField(to=Area, db_table='hinnox_ideas_technologies')
    privacy_setting = models.ForeignKey(to=PrivacySetting, blank=True, null=True, on_delete=models.PROTECT,
                                        help_text='Quyền riêng tư cho ý tưởng')

    class Meta:
        db_table = 'hinnox_ideas'

    def __str__(self):
        if len(self.title) <= 50:
            return self.title
        return self.title[:50]
