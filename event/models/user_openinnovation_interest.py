from django.db import models


class UserOpenInnovationInterest(models.Model):
    user = models.ForeignKey(to='main.User', on_delete=models.CASCADE,
                             help_text='User interested in an open innovation')
    open_innovation = models.ForeignKey(to='main.OpenInnovation', on_delete=models.CASCADE,
                                        help_text='Open innovation which user has interested in')
    datetime_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hinnox_user_openinnovation_interest'
        unique_together = ['user', 'open_innovation']
