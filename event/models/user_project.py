from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from models.base import BaseModel


class UserProject(BaseModel):
    user = models.ForeignKey(to='main.User', on_delete=models.CASCADE, help_text='Project User')
    title = models.CharField(max_length=255, help_text='Title of the project')
    description = models.TextField(blank=True, null=True, help_text='Description of the project')
    category = models.ForeignKey(to='main.Category', blank=True, null=True, on_delete=models.SET_NULL,
                                 help_text='Category of the project')
    persons = models.IntegerField(blank=True, null=True, help_text='Number of people participating in the project ')

    class Status(models.TextChoices):
        PLANNED = 'PLANNED', 'Planned'
        ONGOING = 'ONGOING', 'Ongoing'
        FINISHED = 'FINISHED', 'Finished'
        STOPPED = 'STOPPED', 'Stopped'
    status = models.CharField(max_length=8, choices=Status.choices, default=Status.PLANNED,
                              help_text='Status of the project - Planned - Ongoing - Finished - Stopped')
    progress = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)],
                                   help_text='Progress of the project')
    project_link = models.URLField(blank=True, null=True, help_text='Link of the project')
    due_date = models.DateField(blank=True, null=True, help_text='Due date of the project')

    class Meta:
        db_table = 'hinnox_user_project'
        verbose_name = 'User Project'
        verbose_name_plural = 'User Projects'

    def __str__(self):
        return f'{self.title}'

    def get_images(self):
        return [media.build_url() for media in self.media_set.all()]

    def delete(self, *args, **kwargs):
        self.media_set.all().delete()
        return super(UserProject, self).delete(*args, **kwargs)
