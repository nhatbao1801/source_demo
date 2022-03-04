from django.db import models
from .job import Job
from .area import Area


class JobSkill(models.Model):
    job = models.ForeignKey(to=Job, on_delete=models.CASCADE)
    area = models.ForeignKey(to=Area, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'hinnox_jobs_skills'

    def __str__(self):
        return self.area.name
