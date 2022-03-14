#  Copyright (c) 2020
#  Team hspaces.net
#  Contributors sang.tanhle, HuynhDH

from rest_framework import serializers

from models import ModuleLesson
from utils import get_translate


class ModuleLessonSerializer(serializers.ModelSerializer):
    course_module_info = serializers.SerializerMethodField(read_only=True)
    learned = serializers.SerializerMethodField(read_only=True)
    views_time = serializers.SerializerMethodField(read_only=True)
    pause_timestamp = serializers.SerializerMethodField(read_only=True)
    v_current_view = serializers.SerializerMethodField(read_only=True)
    v_view_id = serializers.SerializerMethodField(read_only=True)
    title_vi = serializers.SerializerMethodField(method_name='get_title_vi', read_only=True)
    title_en = serializers.SerializerMethodField(method_name='get_title_en', read_only=True)
    attachments = serializers.SerializerMethodField()

    class Meta:
        model = ModuleLesson
        fields = '__all__'
        extra_kwargs = {
            'course_module': {
                'write_only': True
            }
        }

    def get_course_module_info(self, obj):
        return {
            'id': obj.course_module.id,
            'name': obj.course_module.name
        }

    def get_learned(self, inst):
        data = inst.modulelessonviewed_set.filter(user_id=self.context['request'].user) if self.context.get(
            'request') else None
        return True if data and data.first().views_time > 0 else False

    def get_views_time(self, inst):
        data = inst.modulelessonviewed_set.filter(user_id=self.context['request'].user) if self.context.get(
            'request') else None
        return data.first().views_time if data else 0

    def get_pause_timestamp(self, inst):
        data = inst.modulelessonviewed_set.filter(user_id=self.context['request'].user) if self.context.get(
            'request') else None
        return data.first().pause_timestamp if data else 0

    def get_v_current_view(self, inst):
        data = inst.modulelessonviewed_set.filter(user_id=self.context['request'].user) if self.context.get(
            'request') else None
        return data.first().current_view if data else False

    def get_v_view_id(self, inst):
        data = inst.modulelessonviewed_set.filter(user_id=self.context['request'].user) if self.context.get(
            'request') else None
        return data.first().id if data else None

    def get_title_vi(self, inst):
        trans = inst.translate_set.all()
        title_vi = get_translate(_objects=trans, _field='title', _language_id=1)
        return title_vi if title_vi else inst.title

    def get_title_en(self, inst):
        trans = inst.translate_set.all()
        title_en = get_translate(_objects=trans, _field='title', _language_id=2)
        return title_en

    def get_attachments(self, inst):
        request = self.context.get('request')
        list_attachment_url = list()
        for attach in inst.modulelessonattachment_set.all():
            file = attach.attachment
            if request:
                list_attachment_url.append({'id': attach.id,
                                            'path': request.build_absolute_uri(file)})
            else:
                list_attachment_url.append({'id': attach.id,
                                            'path': file.url})
        return list_attachment_url
