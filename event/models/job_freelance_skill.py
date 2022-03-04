from django.db import models
from .job_freelance import JobFreelance
from .area import Area


class JobFreelanceSkill(models.Model):
    job_freelance = models.ForeignKey(to=JobFreelance, on_delete=models.CASCADE)
    area = models.ForeignKey(to=Area, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'hinnox_jobs_freelance_skills'

    def __str__(self):
        return self.area.name
