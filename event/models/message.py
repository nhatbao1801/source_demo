from django.db import models
from .invitation import Invitation
from .user import User


class Message(models.Model):
    """
    Hộp thoại tin nhắn
    """
    from_invitation = models.ForeignKey(to=Invitation, blank=True, null=True, on_delete=models.CASCADE)
    from_user = models.ForeignKey(to=User, related_name='messages_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(to=User, related_name='messages_recieved', on_delete=models.CASCADE)
    content = models.TextField(help_text='Nội dung tin nhắn')
    STATUS = [
        ('read', 'Đã xem'),
        ('unread', 'Chưa xem'),
        ('pending', 'Đang chờ'),
    ]
    status = models.CharField(max_length=10, choices=STATUS, help_text='Trạng thái tin nhắn')
    datetime_sent = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hinnox_messages'

    def __str__(self):
        if len(self.content) <= 50:
            return self.content
        return self.content[:50]
