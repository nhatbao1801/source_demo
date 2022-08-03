import uuid
from django.db import models
from event.models.base_model import BaseModel
from django.utils.timezone import now

class EventParticipant(BaseModel):
    class StageJoin(models.TextChoices):
        INVITED = 'INVITED', ('INVITED')
        JOINED = 'JOINED', ('JOINED')

    event = models.ForeignKey(to='event.Event', help_text='Event', blank=True, null=True, on_delete=models.CASCADE)
    uid = models.CharField(max_length=100 ,blank=True, null=True, help_text="Người được mời")
    inviter_id = models.CharField(max_length=100 ,blank=True, null=True, help_text='Người mời tham gia')
    stage = models.CharField(max_length=10, choices=StageJoin.choices, default=StageJoin.JOINED)
    code = models.CharField(max_length=100 ,blank=True, null=True)

    class Meta:
        db_table = 'event_participant'
        verbose_name = 'Event participant'
        verbose_name_plural = 'Event participants'


    def save(self, *args, **kwargs):
        self.code = uuid.uuid4()
        super(EventParticipant, self).save(*args, **kwargs)