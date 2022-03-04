from django.db import models


class Role(models.Model):
    """
    Vai trò của người dùng trong công việc
    """
    name = models.CharField(max_length=55, help_text='CE0, CIO, CTO, CFO, Founder, Co-Founder, Admin etc.')

    class Meta:
        verbose_name = 'vai trò'
        verbose_name_plural = 'Role - Vai trò'
        db_table = 'hinnox_roles'

    def __str__(self):
        return self.name
