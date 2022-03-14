from django.db import models
from .event import Event


class Ticket(models.Model):
    event = models.ForeignKey(to=Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, help_text='Dành cho đối tượng nào Participant, Developer, Designer, Tự thêm')
    description = models.CharField(max_length=300, blank=True, null=True, help_text='Mô tả sự kiện')
    sale_from = models.DateTimeField(help_text='Ngày mở bán')
    sale_to = models.DateTimeField(help_text='Ngày kết thúc')
    max_quantity = models.PositiveSmallIntegerField(help_text='Số lượng tối đa có thể tham dự')
    sold = models.PositiveSmallIntegerField(help_text='Số lượng đã bán')
    price = models.DecimalField(max_digits=20, decimal_places=3, help_text='Giá của vé')

    class Meta:
        db_table = 'hinnox_tickets'

    def __str__(self):
        return self.name
