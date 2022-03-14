from django.db import models


class OrganizationType(models.Model):
    name = models.CharField(max_length=100, help_text='Loại hình tổ chức ví dụ Fund, Institute, Accelerator')
    code = models.CharField(max_length=100, blank=True, null=True, help_text='Code của loại hình tổ chức')

    class Meta:
        verbose_name = 'loại hình tổ chức'
        verbose_name_plural = 'OrganizationType - Loại hình tổ chức'
        db_table = 'hinnox_organization_types'

    def __str__(self):
        return self.name
