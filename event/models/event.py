from cloudinary.models import CloudinaryField
from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now

from .area import Area
from .base import BaseModel
from .city import City
from .event_type import EventType


class Event(BaseModel):
    city = models.ForeignKey(to=City, blank=True, null=True, on_delete=models.CASCADE, help_text='Thành phố noi tổ chức sự kiện')
    type = models.ForeignKey(to=EventType, blank=True, null=True, on_delete=models.CASCADE, help_text='Loại sự kiện')
    areas = models.ManyToManyField(to=Area, blank=True, db_table='hinnox_events_areas')
    name = models.CharField(max_length=1000, help_text='Tên của sự kiện')
    date_created = models.DateTimeField(help_text='Ngày tạo', auto_now_add=True)
    picture = CloudinaryField('image', blank=True, null=True, help_text='File ảnh')
    picture_url = models.URLField(blank=True, null=True, help_text='URL ảnh đại diện của sự kiện')
    url = models.CharField(max_length=300, blank=True, null=True,
                           help_text='Địa chỉ tùy chỉnh đến trang của sự kiện https://hinnox.com/event-url')
    hash_tag = models.CharField(max_length=150, blank=True, null=True,
                                help_text='Tìm kiếm sự kiện trên các mạng xã hội khác')
    # map_point = gis_models.PointField(help_text='Location point trên map', null=True, blank=True)
    street_address = models.CharField(max_length=512, blank=True, null=True, help_text='Địa chỉ chi tiết của sự kiện')
    venue = models.CharField(max_length=300, blank=True, null=True, help_text='Tên địa điểm tổ chức sự kiện')
    tagline = models.CharField(max_length=100, blank=True, null=True, help_text='Tag giúp tìm kiếm event trong hinnox')
    description = models.CharField(max_length=2500, blank=True, null=True, help_text='Mô tả về sự kiện')
    from_date = models.DateTimeField(blank=True, null=True, help_text='Ngày bắt đầu')
    to_date = models.DateTimeField(blank=True, null=True, help_text='Ngày kết thúc')
    schedule = models.TextField(blank=True, null=True, help_text='Kế hoạch tổ chức của sự kiện')
    users_interested_in = models.ManyToManyField(to='event.User', help_text='User quan tâm tới sự kiện', blank=True)
    last_modified = models.DateTimeField(help_text='Thời gian sửa đổi lần cuối', blank=True, null=True)

    class Meta:
        db_table = 'hinnox_events'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.url is None:
            from datetime import datetime
            self.url = slugify(self.name) + '-' + str(abs(hash(datetime.now())))
        if self.pk is not None and not self.team and not self.organization:
            raise ValueError("Updating the value of creator isn't allowed")
        self.last_modified = now()
        super().save(*args, **kwargs)

    def get_owner(self):
        if self.team is not None:
            return self.team
        if self.organization is not None:
            return self.organization

    def get_picture_url(self):
        return self.picture.build_url() if self.picture else ''
