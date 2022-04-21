import uuid
from django.db import models
from event.models.base_model import BaseModel
from django.utils.timezone import now

class EventParticipant(BaseModel):
    class StageJoin(models.TextChoices):
        INVITED = 'INVITED', ('INVITED')
        JOINED = 'JOINED', ('JOINED')

    event = models.ForeignKey(to='event.Event', help_text='Event', blank=True, null=True, on_delete=models.CASCADE)
    uid = models.ForeignKey(to='account.RefAccount', help_text='Người tham gia', blank=True, null=True, related_name="%(app_label)s_%(class)s_uid", on_delete=models.CASCADE)
    inviter_id = models.ForeignKey(to='account.RefAccount', help_text='Người mời tham gia', blank=True, null=True, related_name="%(app_label)s_%(class)s_inviter", on_delete=models.CASCADE)
    stage = models.CharField(max_length=10, choices=StageJoin.choices, default=StageJoin.JOINED)
    code = models.CharField(max_length=100 ,blank=True, null=True)

    class Meta:
        db_table = 'event_participant'
        verbose_name = 'Event participant'
        verbose_name_plural = 'Event participants'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.code = uuid.uuid4()
        super(EventParticipant, self).save(*args, **kwargs)