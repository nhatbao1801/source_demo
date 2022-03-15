import cloudinary
from cloudinary.models import CloudinaryField
from django.db import models

from event.models.event import Event


class Media(models.Model):
    event = models.ForeignKey(to=Event, blank=True, null=True, on_delete=models.CASCADE)

    class Type(models.TextChoices):
        VIDEO = 'vid', 'video'
        IMAGE = 'img', 'image'

    media_type = models.CharField(max_length=7, choices=Type.choices, help_text='Loại media muốn lưu')
    url = models.CharField(max_length=300, blank=True, null=True, help_text='Nếu chọn loại media là video')
    image = CloudinaryField('image', blank=True, null=True, help_text='File ảnh')
    description = models.CharField(max_length=255, blank=True, null=True, help_text='Mô tả file')
    set_as_cover = models.BooleanField(default=False, help_text='Chọn ảnh làm ảnh bìa hay không?')
    ref = models.CharField(max_length=255, blank=True, null=True,
                           help_text='Ref: trường hợp không có thuộc id nào thì truyền định danh: vd: application_form')

    class Meta:
        db_table = 'hinnox_medias'

    def __str__(self):
        return str(self.id)

    def get_image_url(self, *args, **kwargs):
        """Build image url with https"""
        return self.image.build_url(secure=True,
                                    crop='thumb') if self.image is not None else None

    def delete(self, *args, **kwargs):
        if self.image:
            cloudinary.api.delete_resources(self.image.public_id)
        return super(Media, self).delete(*args, **kwargs)