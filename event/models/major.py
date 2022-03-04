from django.db import models


class Major(models.Model):
    name = models.CharField(max_length=512, verbose_name='Tên', help_text='Tên chuyên ngành')

    class Meta:
        db_table = 'hinnox_majors'
        verbose_name = 'chuyên ngành'
        verbose_name_plural = 'Major - Chuyên ngành'

    def __str__(self):
        return self.name
