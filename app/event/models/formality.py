from django.db import models
from event.models.base_model import BaseModel


class Formality(BaseModel):
    name = models.CharField(max_length=255, help_text='Formality name')
    code = models.CharField(max_length=255, help_text='Formality code')


    class Meta:
        db_table = 'formality'
        verbose_name = 'formality'
        verbose_name_plural = 'formality'

    def __str__(self):
        return self.name