#  Copyright (c) 2020
#  Team hspaces.net
#  Contributors sang.tanhle, HuynhDH
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from cloudinary.models import CloudinaryField

from role import Role
from user import User
from area import Area
from utils import generate_secret_key
from validators import validate_course_level


class Course(models.Model):
    course_category_id = models.ForeignKey(to='hSchool.CourseCategory', on_delete=models.PROTECT,
                                           blank=True, null=True,
                                           help_text=_('course category'))
    course_subcategory = models.ForeignKey(to='hSchool.CourseSubCategory', on_delete=models.PROTECT,
                                           blank=True, null=True,
                                           help_text=_('course sub category'))
    skills_accquired = models.ManyToManyField(to=Area, db_table='hschool_course_skill_accquired',
                                              help_text=_('skills which are the course brought to user'))
    users_join = models.ManyToManyField(to=User, through='JoinedCourse', through_fields=('course', 'user'),
                                        help_text=_('Set of users has joined a course'))
    instructors = models.ManyToManyField(to=User, related_name='instructed_courses',
                                         through='CourseInstructor', through_fields=('course', 'user'))
    thumb = CloudinaryField(folder='/course/thumb', null=True, blank=False)
    slug = models.SlugField(max_length=250, default='', help_text=_('slug of course'))

    class LevelChoices(models.TextChoices):
        BEGINER = 'Beginer', 'Beginer'
        INTERMIDATE = 'Intermediate', 'Intermediate'
        ADVANCE = 'Advance', 'Advance'

    level = models.CharField(max_length=25, choices=LevelChoices.choices, help_text=_('course level'),
                             validators=[validate_course_level])
    online_hours = models.SmallIntegerField(help_text=_('online hours for the course'))
    about = models.TextField(help_text=_('about the course'))
    career_orientation = models.TextField(help_text=_('career orientation'))
    title = models.TextField(help_text=_('title'))
    benefits = models.ManyToManyField(to='Benefit')
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    creator = models.ForeignKey(to=User, related_name='course_creator', help_text=_('Course creator'), blank=True,
                                null=True, on_delete=models.CASCADE)

    course_for = models.ManyToManyField(to=Role, db_table='hschool_course_course_for', related_name='course_for',
                                        help_text=_('Course for'))
    video_url_introduce = models.CharField(max_length=500, blank=True, null=True,
                                           help_text=_('Link video giới thiệu khóa học'))

    class StateChoices(models.TextChoices):
        APPROVED = 'Approved', 'Approved'
        PENDING = 'Pending', 'Pending'
        DENIED = 'Denied', 'Denied'

    state = models.CharField(max_length=50, default='Pending', choices=StateChoices.choices,
                             help_text=_('Course approval'))

    price = models.DecimalField(max_digits=8, decimal_places=2, help_text=_('Price'), blank=True, null=True)
    users_favorite = models.ManyToManyField(to='main.User', related_name='favorite_course', blank=True)

    @property
    def price_display(self):
        return "%s" % self.price

    class Meta:
        db_table = 'hschool_course'
        verbose_name = _('course')
        verbose_name_plural = _('courses')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f'{slugify(self.title)}-{generate_secret_key(nbyte=10, s_type="token_urlsafe")}'
        return super(Course, self).save(*args, **kwargs)

    def get_thumb_image(self, **kwargs):
        width = kwargs.get('width')
        height = kwargs.get('height')
        width = width if width is not None else 240
        height = height if height is not None else 240
        return self.thumb.build_url(width=width, height=height, secure=True,
                                    crop='thumb') if self.thumb is not None else None
