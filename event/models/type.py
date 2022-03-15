from cloudinary.models import CloudinaryField
from django.db import models
from django.utils.translation import gettext_lazy as _


class Type(models.Model):
    """ Type model -  Các định danh nghề nghiệp """
    name = models.CharField(max_length=255, verbose_name=_('Name'), help_text=_('backend-dev, front-end dev etc.'), null=True)
    category = models.ForeignKey(to='main.Category', blank=True, null=True, on_delete=models.CASCADE, verbose_name=_('Category'), help_text=_('Category'))
    thumb = CloudinaryField(folder='/type/thumb', null=True, blank=True, verbose_name=_('thumb'), help_text=_('Thumbnail of type'))

    class Meta:
        # db_table = 'hinnox_types'
        db_table = 'hinnox_types'
        verbose_name = _('Type')
        verbose_name_plural = _('Types')

    def __str__(self):
        """Return name of type"""
        return self.name

    @property
    def get_thumb_image(self, **kwargs):
        if not self.thumb:
            return None
        if not kwargs.get('width') or not kwargs.get('height'):
            return self.thumb.build_url(crop='thumb', secure=True)
        return self.thumb.build_url(width=kwargs.get('width'), height=kwargs.get('height'), secure=True, crop='thumb')
