from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=50, verbose_name='Tên vị trí',
                            help_text='Enployee,'
                                      'Intern,Advisor,Investor,follower,Speaker,Mentors,Organizers etc')

    class Meta:
        db_table = 'hinnox_positions'
        verbose_name = 'vị trí'
        verbose_name_plural = 'Position - Vị trí'

    def __str__(self):
        return self.name
