from datetime import datetime

# from django.contrib.gis.db import models as gis_models
from cloudinary.models import CloudinaryField
from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now

from .city import City
from .organization_type import OrganizationType


class Organization(models.Model):
    user = models.ForeignKey(to='User', on_delete=models.DO_NOTHING)
    type = models.ForeignKey(to=OrganizationType, on_delete=models.DO_NOTHING)
    city = models.ForeignKey(to=City, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=1000, help_text="Tên của tổ chức")
    picture = CloudinaryField('image', blank=True, null=True, help_text='File ảnh')
    picture_url = models.URLField(blank=True, null=True, help_text='URL ảnh đại diện của tổ chức')
    # map_point = gis_models.PointField(help_text='Location point trên map', null=True, blank=True)
    street_address = models.CharField(max_length=255, blank=True, null=True, help_text='Địa chỉ chi tiết của tổ chức')
    url = models.CharField(max_length=300, blank=True, null=True, db_index=True,
                           help_text='Địa chỉ tùy chỉnh đến trang của tổ chức https://hinnox.com/organization-url')
    tagline = models.CharField(max_length=100, blank=True, null=True,
                               help_text='Tag giúp tìm kiếm tổ chức trong hinnox')
    description = models.CharField(max_length=2500, blank=True, null=True, help_text='Mô tả tổng quan về tổ chức')
    last_modified = models.DateTimeField(help_text='Thời gian sửa đổi lần cuối', blank=True, null=True)

    class Meta:
        db_table = 'hinnox_organizations'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.url is None:
            self.url = slugify(self.name) + '-' + str(abs(hash(datetime.now())))
        self.last_modified = now()

        return super().save()

    def get_picture_url(self, **kwargs):
        return self.picture.build_url(secure=True) if self.picture else None
