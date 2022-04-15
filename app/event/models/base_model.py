from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(to="account.RefAccount", related_name="%(app_label)s_%(class)s_created_by", blank=True, null=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(to="account.RefAccount", related_name="%(app_label)s_%(class)s_updated_by", blank=True, null=True, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    deleted_by = models.ForeignKey(to="account.RefAccount", related_name="%(app_label)s_%(class)s_deleted_by", blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        abstract = True
