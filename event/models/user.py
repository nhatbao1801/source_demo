from datetime import datetime

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.text import slugify
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from .team import Team
from .organization import Organization
from .contest import Contest
from .event import Event
from .job import Job
from .status import Status
from .setting import Setting
from .area import Area
from .position import Position


class User(AbstractUser):
    # Recommendation
    teams_ask_for_recommendation = models.ManyToManyField(
        to=Team, related_name='ask_users_for_recommendation', help_text='Các nhóm đề nghị user giới thiệu',
        through='Recommendation', through_fields=('user_being_ask', 'team_ask_for')
    )
    organizations_ask_for_recommendation = models.ManyToManyField(
        to=Organization, related_name='ask_users_for_recommendation', help_text='Các tổ chức đề nghị user giới thiệu',
        through='Recommendation', through_fields=('user_being_ask', 'organization_ask_for')
    )
    contests_ask_for_recommendation = models.ManyToManyField(
        to=Contest, related_name='ask_users_for_recommendation', help_text='Các tổ chức đề nghị user giới thiệu',
        through='Recommendation', through_fields=('user_being_ask', 'contest_ask_for')
    )
    ask_others_for_recommendation = models.ManyToManyField(
        to='self', symmetrical=False, related_name='ask_users_for_recommendation',
        help_text='Các người dùng khác đề nghị user giới thiệu',
        through='Recommendation', through_fields=('user_ask_for', 'user_being_ask')
    )
    # Following
    following_teams = models.ManyToManyField(
        to=Team, related_name='users_following', help_text='Tập các team mà người dùng theo dõi',
        through='Following', through_fields=('from_user', 'to_team')
    )
    following_organizations = models.ManyToManyField(
        to=Organization, related_name='users_following', help_text='Tập các tổ chức mà người dùng theo dõi',
        through='Following', through_fields=('from_user', 'to_organization')
    )
    following_contests = models.ManyToManyField(
        to=Contest, related_name='users_following', help_text='Tập các cuộc thi mà người dùng theo dõi',
        through='Following', through_fields=('from_user', 'to_contest')
    )
    following_events = models.ManyToManyField(
        to=Event, related_name='users_following', help_text='Tập các sự kiện mà người dùng theo dõi',
        through='Following', through_fields=('from_user', 'to_event')
    )
    following_other_users = models.ManyToManyField(
        to='self', related_name='users_following',
        help_text='Tập các người dùng khác đang theo dõi người dùng hiện tại',
        through='Following', through_fields=('from_user', 'to_user')
    )
    # Chat
    jobs_chat = models.ManyToManyField(
        to=Job, related_name='chat_users', through='JobChat', through_fields=('user', 'job'),
        help_text='Tập các job mà user nhắn tin'
    )
    # Privacy settings for user
    privacy_settings = models.ManyToManyField(to='PrivacySetting', related_name='users', related_query_name='user',
                                              db_table='hinnox_privacy_settings_users')

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=False,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    # Status
    status = models.ManyToManyField(to=Status, db_table='hinnox_user_status')
    # Setting
    setting = models.OneToOneField(to=Setting, blank=True, null=True, on_delete=models.SET_NULL)
    # Heat
    posts_heat = models.ManyToManyField(to='Post', related_name='users_heat', through='Heat')
    kpis_heat = models.ManyToManyField(to='KPI', related_name='users_heat', through='Heat')
    # Skill
    skills = models.ManyToManyField(to=Area, db_table='hinnox_users_skills')
    # Interest
    interests = models.ManyToManyField(to=Position, db_table='hinnox_talent_interests')

    email = models.EmailField(_('email address'), blank=False, unique=True)
    picture = CloudinaryField('image', blank=True, null=True, help_text='File ảnh')
    picture_url = models.URLField(blank=True, null=True, help_text='URL của ảnh đại diện của bạn')
    short_bio = models.CharField(max_length=2500, blank=True, null=True, help_text='Mô tả ngắn về bản thân')
    url = models.CharField(max_length=300, blank=True, null=True, db_index=True, unique=True,
                           help_text='Địa chỉ tùy chỉnh đến trang cá nhân https://hinnox.com/user-url')
    something_great_to_tell = models.TextField(blank=True, null=True,
                                               help_text='Kể về những thứ tuyệt vời mà bạn đã làm được')
    city = models.ForeignKey(to='City', on_delete=models.SET_NULL, related_name='users', blank=True, null=True)

    class GenderChoice(models.TextChoices):
        MALE = 'male', _('MALE')
        FEMALE = 'female', _('FEMALE')
        OTHER = 'other', _('OTHER')

    gender = models.CharField(max_length=6, help_text='Giới tính', choices=GenderChoice.choices, blank=True, null=True)
    phone_num = models.CharField(max_length=12, help_text='Số điện thoại', blank=True, null=True, unique=True)
    last_modified = models.DateTimeField(help_text='Thời gian sửa đổi lần cuối', blank=True, null=True)
    is_premium = models.IntegerField(help_text='Tài khoản premium', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'hinnox_users'
        verbose_name = 'người dùng'
        verbose_name_plural = 'User - Người dùng'

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        """
        Ussername là họ và tên người dùng
        Url của user là slug của username
        :param args:
        :param kwargs:
        :return:
        """
        try:
            self.username = self.first_name + ' ' + self.last_name
            if self.url is None:
                self.url = slugify(self.username) + '-' + str(abs(hash(datetime.now())))
            self.last_modified = now()
            self.picture_url = self.picture.build_url(secure=True, transformation=[
                {'width': 50, 'height': 50, 'crop': 'thumb'}
            ]) if self.picture is not None else None
        except Exception:
            pass
        return super(User, self).save()

    @property
    def get_absolute_url(self):
        return '/'

    def get_picture_url(self, width=50, height=50):
        return self.picture.build_url(secure=True, transformation=[
            {'width': width, 'height': height, 'crop': 'thumb'}
        ]) if self.picture is not None else None

    def get_cover_url(self, *args, **kwargs):
        return self.media_set.filter(
            set_as_cover=True).first().get_image_url() if self.media_set.filter(set_as_cover=True).first() else None
