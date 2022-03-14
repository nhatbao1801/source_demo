#  Copyright (c) 2020
#  Team hspaces.net
#  Contributors sang.tanhle, HuynhDH
from django.utils.translation import gettext_lazy as _
from django.contrib.humanize.templatetags import humanize
from rest_framework import serializers

from models.course_question_answer import CourseQuestionAnswer


class CourseQuestionAnswerSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField(read_only=True)
    lesson_info = serializers.SerializerMethodField(read_only=True)
    human_time = serializers.SerializerMethodField(read_only=True)
    c_comment = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CourseQuestionAnswer
        fields = '__all__'

    def get_lesson_info(self, inst):
        if not inst.module_lesson:
            return {}
        return {
            'id': inst.module_lesson.id,
            'title': inst.module_lesson.title,
        }

    def get_user_info(self, inst):
        if not inst.user:
            return {}
        return {
            'id': inst.user.id,
            'username': inst.user.username,
            'url': inst.user.url,
            'email': inst.user.email,
            'picture': inst.user.picture.build_url() if inst.user.picture is not None else None
        }

    def get_c_comment(self, inst):
        return inst.comment_set.count() if inst.comment_set else 0

    def get_human_time(self, inst):
        return _(humanize.naturaltime(inst.date_created)) if inst.date_created else None
