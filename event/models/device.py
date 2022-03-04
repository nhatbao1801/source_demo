#  Copyright (c) 2020
#  Team hspaces.net
#  Contributors sang.tanhle, HuynhDH

from django.db import models
from django.utils.translation import gettext_lazy as _


class Device(models.Model):
    user = models.ForeignKey(to='User', on_delete=models.CASCADE)
    # Device registration_token for recieving firebase cloud messaging
    device_registration_token_fcm = models.CharField(max_length=512,
                                                     help_text=_('Device registration token for recieving FCM'))
    last_modified = models.DateTimeField(auto_now=True,
                                         help_text=_('Last time modified of the device registration token'), blank=True,
                                         null=True)

    class DeviceType(models.TextChoices):
        IOS = 'IOS', 'IOS Device'
        Android = 'Android', 'Android Device'
        Web = 'Web', 'Web application'

    device_type = models.CharField(max_length=12, choices=DeviceType.choices, blank=True, null=True,
                                   help_text=_('Device type'))

    class Meta:
        db_table = 'hinnox_device_registration_fcm'
