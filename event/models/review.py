from django.db import models
from .deal import Deal
from .user import User


class Review(models.Model):
    deal = models.ForeignKey(to=Deal, on_delete=models.PROTECT)
    user = models.ForeignKey(to=User, on_delete=models.PROTECT)
    content = models.CharField(max_length=1000, help_text='Nội dung review')

    class Meta:
        db_table = 'hinnox_reviews'
