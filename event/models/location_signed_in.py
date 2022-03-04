from django.db import models
from .user import User


class LocationSignedIn(models.Model):
    """
    Thông tin đăng nhập thiết bị
    """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    device = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True, help_text='Tên vị trí')
    ip = models.GenericIPAddressField(blank=True, null=True, help_text='Địa chỉ ip')
    last_login = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hinnox_locations_signed_in'
