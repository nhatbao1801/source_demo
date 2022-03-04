from django.db import models

from models.base import BaseModel


class UserCV(BaseModel):
    name = models.CharField(max_length=100, blank=True, null=True, help_text='Name')
    user = models.ForeignKey(to='main.User', help_text='User', on_delete=models.CASCADE)
    document = models.ForeignKey(to='main.Document', help_text='Document', on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'hinnox_curriculum_vitae_user'
        verbose_name = 'Curriculum Vitae User'
        verbose_name_plural = 'Curriculum Vitae Users'

    def __str__(self):
        return self.name