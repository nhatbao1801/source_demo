from django.db import models


class BaseModel(models.Model):
    """BaseModel models"""
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    created_by = models.ForeignKey(to='main.User', on_delete=models.CASCADE, related_name='%(class)s_created_by', blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated_by = models.ForeignKey(to='main.User', on_delete=models.CASCADE, blank=True, null=True,
                                   related_name='%(class)s_updated_by')

    class Meta:
        """Meta class"""
        abstract = True
