#  Copyright (c) 2021
#  Team hspaces.net
#  Contributors sang.tanhle, HuynhDH

from django.db import models
from django.utils.translation import gettext_lazy as _
from utils import generate_secret_key


class Notification(models.Model):
    user = models.ForeignKey('main.User', blank=True, null=True, on_delete=models.CASCADE,
                             help_text=_('user who recieved the notification'))
    id = models.CharField(max_length=16, primary_key=True, help_text=_('id of the notification'))
    sender = models.ForeignKey('main.User', blank=True, null=True, related_name='my_sent_notification_set',
                               on_delete=models.CASCADE)
    avatar = models.URLField(blank=True, null=True, help_text=_('avatar who sent the notification'))
    content = models.TextField(blank=True, null=True, help_text=_('content of the notification'))
    message = models.TextField(blank=True, null=True, help_text=_('message of the notification'))
    type = models.CharField(max_length=255, blank=True, null=True, help_text=_('type of the notification'))
    location = models.CharField(max_length=255, blank=True, null=True, help_text=_('location of the notification'))
    datetime_sent = models.DateTimeField(auto_now_add=True, help_text=_('datetime when the notification sent'))

    def __str__(self):
        return self.content

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_secret_key(8)
        return super(Notification, self).save()
