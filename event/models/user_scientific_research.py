import cloudinary
from cloudinary.models import CloudinaryField
from django.db import models

from models.base import BaseModel


class UserScientificResearch(BaseModel):
    user = models.ForeignKey(to='main.User', on_delete=models.CASCADE, help_text='User Scientific Research')
    title = models.CharField(max_length=255, help_text='Title of the scientific research')
    description = models.TextField(blank=True, null=True, help_text='Description of the scientific research')
    picture = CloudinaryField('image', blank=True, null=True, help_text='File image')
    reference_link = models.URLField(blank=True, null=True, help_text='Reference link of the certificate')

    class Meta:
        db_table = 'hinnox_user_scientific_research'
        verbose_name = 'User Scientific Research'
        verbose_name_plural = 'User Scientific Research'

    def __str__(self):
        return f'{self.title}'

    def delete(self, *args, **kwargs):
        # delete picture on cloudinary
        if self.picture:
            cloudinary.api.delete_resources(self.picture.public_id)
        # delete documents
        self.document_set.all().delete()
        return super(UserScientificResearch, self).delete(*args, **kwargs)

    def get_picture_url(self):
        return self.picture.build_url() if self.picture else None
