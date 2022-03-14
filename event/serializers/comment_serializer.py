#  Copyright (c) 2020
#  Team hspaces.net
#  Contributors sang.tanhle, HuynhDH

from rest_framework import serializers

# from hSchool.serializers import CourseSerializer
# from hSchool.serializers.course_announcement_serializer import CourseAnnouncementSerializer
# from hSchool.serializers.course_question_answer_serializer import CourseQuestionAnswerSerializer
# from main.models import Comment
# from main.serializers.open_innovation_serializer import OpenInnovationOutSerializer
# from main.serializers.reply_serializer import ReplySerializer
from serializers.comment_serializer import CourseSerializer
from serializers.course_announcement_serializer import CourseAnnouncementSerializer
from serializers.course_question_answer_serializer import CourseQuestionAnswerSerializer
from models.comment import Comment
from serializers.open_innovation_serializer import OpenInnovationOutSerializer
from reply_serializer import ReplySerializer
from startup.serializers.kpi_serializer import KPISerializer


class CommentSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()
    owner_info = serializers.SerializerMethodField()
    reply_info = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
            'user': {'write_only': True},
            'post': {'write_only': True},
            'kpi': {'write_only': True},
            'course': {'write_only': True},
            'course_announcement': {'write_only': True},
            'course_question_answer': {'write_only': True},
        }

    def get_owner_info(self, inst):
        _data = {}
        if inst.kpi_id:
            _data = KPISerializer(inst.kpi).data
        elif inst.post_id:
            _data = {
                'id': inst.post_id,
                'content': inst.post.content
            }
        elif inst.course_id:
            _data = CourseSerializer(inst.course).data
        elif inst.course_announcement_id:
            _data = CourseAnnouncementSerializer(inst.course_announcement).data
        elif inst.course_question_answer_id:
            _data = CourseQuestionAnswerSerializer(inst.course_question_answer).data
        elif inst.open_innovation_id:
            _data = {}
        return _data

    def get_user_info(self, inst):
        return {
            'id': inst.user.id,
            'username': inst.user.username,
            'url': inst.user.url,
            'email': inst.user.email,
            'picture': inst.user.picture.build_url() if inst.user.picture is not None else None
        }

    def get_reply_info(self, inst):
        return ReplySerializer(inst.reply_set.all(), many=True).data
