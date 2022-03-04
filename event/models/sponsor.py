from django.db import models
from cloudinary.models import CloudinaryField


class Sponsor(models.Model):
    """
    Các nhà tài trợ cho các sự kiện
    """
    logo = CloudinaryField('image', blank=True, null=True, help_text='logo nhà tài trợ')
    name = models.CharField(max_length=255, help_text='Tên nhà tài trợ')
    is_verified = models.BooleanField(default=True, help_text='Nhà tài trợ đã được xác nhận hay chưa')

    class Meta:
        db_table = 'hinnox_sponsors'
        verbose_name = 'Sponsor'
        verbose_name_plural = 'Sponsors'

    def __str__(self):
        return self.name
