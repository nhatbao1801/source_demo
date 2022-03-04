from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now

from .team import Team
from .type import Type


class Deal(models.Model):
    team = models.ForeignKey(to=Team, on_delete=models.PROTECT)
    types = models.ManyToManyField(to=Type, db_table='hinnox_deal_type', help_text='Lĩnh vực của deal đang thực hiện')
    title = models.CharField(max_length=512, help_text='Tiêu đề của deal')
    slug = models.SlugField(max_length=512)
    company_url = models.URLField(blank=True, null=True)
    value = models.DecimalField(max_digits=40, decimal_places=3, help_text='Giá trị deal')
    money_saved = models.DecimalField(max_digits=40, decimal_places=3,
                                      help_text='Giá trị tiết kiệm được nếu sử dụng deal')
    is_beta_phase = models.BooleanField(default=False, help_text='Chỉ ra sản phẩm đang trong giai đoạn beta')
    briefly_describe = models.CharField(max_length=2500, blank=True, null=True,
                                        help_text='Mô tả ngắn gọn về deal 2500 từ')
    detail = models.TextField(blank=True, null=True, help_text='Chi tiết về deal')
    everyone = models.BooleanField(default=True,
                                   help_text='Cho phép deal được quảng cáo trực tiếp đến với các người dùng')
    introduce_video_url = models.URLField(blank=True, null=True, help_text='Link video giới thiệu về deal')
    date_created = models.DateTimeField(help_text='Ngày tạo', auto_now_add=True)
    promote_code = models.CharField(max_length=254, blank=True, null=True, help_text='Code giảm giá cho deal')
    limit = models.PositiveIntegerField(blank=-True, null=True, help_text='Giới hạn số lượng khách hàng sử dụng deal')
    email_for_deal_redemption = models.EmailField(help_text='Email phản hồi hoàn trả deal từ khách hàng')
    last_modified = models.DateTimeField(help_text='Thời gian sửa đổi lần cuối', blank=True, null=True)

    class Meta:
        db_table = 'hinnox_deals'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        from utils import generate_secret_key
        if self.slug is not None:
            self.slug = slugify(self.title)[:490] + generate_secret_key(nbyte=10, s_type='token_urlsafe')
        self.last_modified = now()
        return super(Deal, self).save()
