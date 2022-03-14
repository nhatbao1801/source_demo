from datetime import datetime
from django.db import models
# from django.contrib.gis.db import models as gis_models
from django.conf import settings
from cloudinary.models import CloudinaryField
from django.utils.text import slugify
from django.utils.timezone import now

from .base import BaseModel
from .organization import Organization
from .city import City


def today():
    """
    :return: Ngày giờ hôm nay theo TIME_ZONE trong settings.py
    """
    import pytz
    date_naive = datetime.today()
    timezone = pytz.timezone(settings.TIME_ZONE)
    date_aware = timezone.localize(date_naive)
    return date_aware


class Contest(BaseModel):
    organization = models.ForeignKey(to=Organization, on_delete=models.CASCADE, help_text='Tổ chức tạo cuộc thi')
    city = models.ForeignKey(to=City, blank=True, null=True, on_delete=models.CASCADE, help_text='Thành phố tổ chức cuộc thi')
    title = models.CharField(max_length=300, help_text='Tiêu đề của cuộc thi')
    # map_point = gis_models.PointField(help_text='Location point trên map', null=True, blank=True)
    street_address = models.CharField(max_length=300, blank=True, null=True, help_text='Địa chỉ chi tiết của cuộc thi')
    picture = CloudinaryField('image', blank=True, null=True, help_text='File ảnh')
    picture_url = models.URLField(max_length=300, blank=True, null=True, help_text='URL ảnh đại diện của cuộc thi')
    tagline = models.CharField(max_length=100, blank=True, null=True,
                               help_text='Tag giúp tìm kiếm cuộc thi trong hinnox')
    description = models.CharField(max_length=2500, blank=True, null=True, help_text='Mô tả về cuộc thi')
    date_created = models.DateTimeField(help_text='Ngày tạo cuộc thi', default=today)
    url = models.CharField(max_length=300, blank=True, null=True,
                           help_text='Địa chỉ tùy chỉnh đến trang của cuộc thi https://hinnox.com/contest-url')
    from_date = models.DateTimeField(help_text='Ngày bắt đầu', null=True, blank=True)
    to_date = models.DateTimeField(help_text='Ngày kết thúc', null=True, blank=True)
    users_interested_in = models.ManyToManyField(to='main.User', blank=True, help_text='User quan tâm tới cuộc thi')
    last_modified = models.DateTimeField(help_text='Thời gian sửa đổi lần cuối', blank=True, null=True)

    class Meta:
        db_table = 'hinnox_contests'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.url is None:
            self.url = slugify(self.title) + '-' + str(abs(hash(datetime.now())))
        self.last_modified = now()
        return super().save()

    def get_picture_url(self):
        return self.picture.build_url() if self.picture else ''
