from django.db import models
from event.models.base_model import BaseModel
from django.utils.timezone import now

class Event(BaseModel):
    owner = models.ForeignKey(to='account.RefAccount', help_text='Người đứng ra tổ chức sự kiện', blank=True, null=True, related_name="%(app_label)s_%(class)s_owner", on_delete=models.CASCADE)
    name = models.CharField(max_length=255, help_text='Event name')
    cover = models.CharField(max_length=255, help_text='Cover name', blank=True, null=True)
    venue = models.CharField(max_length=300, blank=True, null=True, help_text='Tên địa điểm tổ chức sự kiện')
    tagline = models.CharField(max_length=100, blank=True, null=True, help_text='Tag giúp tìm kiếm event trong hinnox')
    description = models.TextField(blank=True, null=True, help_text='Mô tả về sự kiện')
    short_description = models.TextField(blank=True, null=True, help_text='Mô tả ngắn về sự kiện')
    from_date = models.DateTimeField(blank=True, null=True, help_text='Ngày bắt đầu')
    to_date = models.DateTimeField(blank=True, null=True, help_text='Ngày kết thúc')
    users_interested_in = models.ManyToManyField(to='account.RefAccount', help_text='User quan tâm tới sự kiện', blank=True)
    privacy = models.ForeignKey(to="event.Privacy", blank=True, null=True, on_delete=models.CASCADE)
    co_host = models.ManyToManyField(to='account.RefAccount', blank=True, related_name="%(app_label)s_%(class)s_co_hosts")
    formality = models.ForeignKey(to='event.Formality', blank=True, on_delete=models.CASCADE, null=True)
    event_type = models.ForeignKey(to='event.EventType', blank=True, on_delete=models.CASCADE, null=True)
    business_level_code = models.CharField(max_length=300, blank=True, null=True, help_text='Business Level Code')
    

    class Meta:
        db_table = 'event'
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return self.name