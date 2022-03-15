from django.db import models
from .event import Event
from .user import User


class EventParticipant(models.Model):
    event = models.ForeignKey(to=Event, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'hinnox_event_participants'

    def get_owner(self):
        if self.user is not None:
            return self.user
