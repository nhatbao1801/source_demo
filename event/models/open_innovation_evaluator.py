import binascii
import os

from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from .open_innovation import OpenInnovation
from .organization import Organization


def generate_key():
    return binascii.hexlify(os.urandom(15)).decode()


class OpenInnovationEvaluator(models.Model):
    open_innovation = models.ForeignKey(to=OpenInnovation, blank=True, null=True, on_delete=models.SET_NULL)
    evaluator = models.ForeignKey(to=Organization, blank=True, null=True, on_delete=models.SET_NULL,
                                  help_text='Tổ chức trung gian đứng ra đăng các thách thách thức(trong hệ thống gọi là'
                                            'sáng tạo mở)'
                                            'Chỉ có tố chức này tham gia đăng thách '
                                            'thức'
                                            'và đánh giá các giải pháp gửi đến')
    is_accepted = models.BooleanField(blank=True, null=True,
                                      help_text='Tổ chức đóng vai trò là evaluator đã đồng ý chưa')
    request_key = models.CharField(_("Request Key"), default=generate_key, max_length=30, unique=True)
    last_modified = models.DateTimeField(help_text='Thời gian sửa đổi lần cuối', blank=True, null=True)

    class Meta:
        db_table = 'hinnox_open_innovations_evaluators'
        unique_together = ['open_innovation', 'evaluator']

    def save(self, *args, **kwargs):
        if not self.request_key:
            self.request_key = generate_key()
        self.last_modified = now()
        return super().save(*args, **kwargs)
