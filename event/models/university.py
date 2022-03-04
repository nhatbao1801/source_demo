from django.db import models


class University(models.Model):
    name = models.CharField(max_length=512, help_text='Tên trường đại học', verbose_name='tên trường')

    class Meta:
        db_table = 'hinnox_universities'
        verbose_name = 'trường đại học/học viện'
        verbose_name_plural = 'University - Trường đại học/học viện'

    def __str__(self):
        return self.name
