#  Copyright (c) 2020
#  Team hspaces.net
#  Contributors sang.tanhle, HuynhDH

from rest_framework import serializers

from models.course_announcement import CourseAnnouncement


class CourseAnnouncementSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField(read_only=True)
    course_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CourseAnnouncement
        fields = '__all__'

    def get_course_info(self, inst):
        if not inst.course:
            return {}
        return {
            'id': inst.course.id,
            'title': inst.course.title,
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
