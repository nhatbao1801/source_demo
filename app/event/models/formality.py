from django.db import models
from event.models.base_model import BaseModel


class Formality(BaseModel):
    code = models.CharField(primary_key=True, unique=True, max_length=255, help_text='Formality code')
    name = models.CharField(max_length=255, help_text='Formality name')


    class Meta:
        db_table = 'formality'
        verbose_name = 'formality'
        verbose_name_plural = 'formality'

    def __str__(self):
        return self.name