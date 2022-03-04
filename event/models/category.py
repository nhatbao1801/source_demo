from cloudinary.models import CloudinaryField
from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    """Category models"""
    name = models.CharField(max_length=255, verbose_name=_("Category name"), help_text=_("Category name"))
    thumb = CloudinaryField(folder='/category/thumb', null=True, blank=True, verbose_name=_('thumb'), help_text=_('Thumbnail of category'))

    class Meta:
        """Meta Category"""
        db_table = 'hinnox_categories'
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        """Return name without category name"""
        return self.name

    @property
    def get_thumb_image(self, **kwargs):
        if not self.thumb:
            return None
        if not kwargs.get('width') or not kwargs.get('height'):
            return self.thumb.build_url(crop='thumb')
        return self.thumb.build_url(width=kwargs.get('width'), height=kwargs.get('height'), secure=True, crop='thumb')
