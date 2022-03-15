import cloudinary.api
from datetime import datetime

from django.db import models
# from django.contrib.gis.db import models as gis_models
from cloudinary.models import CloudinaryField
from django.urls import reverse
from django.utils.text import slugify
from django.utils.timezone import now

from .stage import Stage
from .support.generate import gen_unique_number


class Team(models.Model):
    unique_id = models.CharField(default=gen_unique_number, max_length=30, unique=True)
    user = models.ForeignKey(to='User', on_delete=models.CASCADE, help_text='Admin của trang')
    stage = models.ForeignKey(to=Stage, null=True, on_delete=models.CASCADE,
                              help_text='Giai đoạn phát triển của một team')
    name = models.CharField(max_length=255, help_text='Tên của nhóm')
    picture = CloudinaryField('image', blank=True, null=True, help_text='File ảnh')
    picture_url = models.URLField(max_length=300, blank=True, null=True, help_text='URL của ảnh đại diện của nhóm')
    url = models.CharField(max_length=300, blank=True, null=True, db_index=True,
                           help_text='Địa chỉ tùy chỉnh đến trang của nhóm https://hinnox.com/team-url')
    founded_date = models.DateTimeField(help_text='Ngày thành lập nhóm', blank=True, null=True)
    tagline = models.CharField(max_length=100, blank=True, null=True, help_text='Tag giúp tìm kiếm team trong hinnox')
    android_app_link = models.URLField(max_length=300, blank=True, null=True, help_text='URL sản phẩm ứng dụng android')
    ios_app_link = models.URLField(max_length=300, blank=True, null=True, help_text='URL sản phẩm ứng dụng ios')
    description = models.CharField(max_length=2500, blank=True, null=True, help_text='Mô tả tổng quan về nhóm')
    is_startup = models.BooleanField(default=False)
    vision = models.TextField(help_text='Tầm nhìn', blank=True, null=True)
    mission = models.TextField(help_text='Sứ mệnh', blank=True, null=True)
    core_value = models.TextField(help_text='Giá trị cốt lỗi', blank=True, null=True)
    # map_point = gis_models.PointField(help_text='Location point trên map', null=True, blank=True)
    phone_num = models.CharField(max_length=12, help_text='Số điện thoại', blank=True, null=True, unique=True)
    street_address = models.CharField(max_length=512, blank=True, null=True, help_text='Địa chỉ chi tiết của team')
    last_modified = models.DateTimeField(help_text='Thời gian sửa đổi lần cuối', blank=True, null=True)

    # Team với mục đích học tập
    use_for_studying = models.BooleanField(default=False, null=True, blank=True, help_text='User for studying')

    class Meta:
        db_table = 'hinnox_teams'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.url is None:
            self.url = slugify(self.name) + '-' + str(abs(hash(datetime.now())))
        self.last_modified = now()
        return super().save()

    def delete(self, *args, **kwargs):
        """Delete remote picture before delete"""
        cloudinary.api.delete_resources(self.picture.public_id)
        return super(Team, self).delete()

    def get_absolute_url(self):
        return reverse('startup:team-profile', kwargs={'team_url': self.url})

    def get_picture_url(self, **kwargs):
        return self.picture.build_url() if self.picture else ''
