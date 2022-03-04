from django.db import models


class SecurityType(models.Model):
    name = models.CharField(max_length=50, help_text='Loại hình chia sẻ cổ phần'
                                                     'Founder share, Convertible Note etc.')

    class Meta:
        db_table = 'hinnox_security_types'

    def __str__(self):
        return self.name
