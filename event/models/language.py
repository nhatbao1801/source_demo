from django.db import models


class Language(models.Model):
    code = models.CharField(max_length=8, verbose_name='Mã ngôn ngữ', help_text='Mã ngôn ngữ ví dụ vi, en-us',
                            unique=True)
    name = models.CharField(max_length=50, verbose_name='Tên ngôn ngữ', help_text = 'Tên ngôn ngữ')

    class Meta:
        db_table = 'hinnox_languages'
        verbose_name = 'ngôn ngữ'
        verbose_name_plural = 'Language - Ngôn ngữ'

    def __str__(self):
        return self.code + f'({self.name})'
