from django.db import models


class TimeZone(models.Model):
    text = models.CharField(max_length=100, help_text='(GMT+07:00) Hanoi')
    value = models.CharField(max_length=100, help_text='Asia/Ho_Chi_Minh')
    gmt = models.CharField(max_length=25, blank=True, null=True, help_text='(GMT+07:00)')

    class Meta:
        db_table = 'hinnox_timezones'
        verbose_name = 'múi giờ'
        verbose_name_plural = 'TImezone - Múi giờ'

    def __str__(self):
        return self.value
