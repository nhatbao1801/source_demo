from django.db import models

from models.base import BaseModel


class UserActivity(BaseModel):
    user = models.ForeignKey(to='main.User', on_delete=models.CASCADE, help_text='Activity User')
    title = models.CharField(max_length=255, help_text='Title of the activity')
    description = models.TextField(blank=True, null=True, help_text='Description of the activity')
    time = models.DateTimeField(help_text='Time of the activity')

    class Meta:
        db_table = 'hinnox_user_activity'
        verbose_name = 'User Activity'
        verbose_name_plural = 'User Activities'

    def __str__(self):
        return f'{self.title}'

    def delete(self, *args, **kwargs):
        self.document_set.all().delete()
        return super(UserActivity, self).delete(*args, **kwargs)