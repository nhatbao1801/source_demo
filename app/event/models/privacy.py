from django.db import models
from event.models.base_model import BaseModel


class Privacy(BaseModel):
    name = models.CharField(max_length=255, help_text='Privacy name')
    code = models.CharField(max_length=255, help_text='Privacy code')


    class Meta:
        db_table = 'privacy'
        verbose_name = 'privacy'
        verbose_name_plural = 'privacy'

    def __str__(self):
        return self.name