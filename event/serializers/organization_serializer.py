#  Copyright (c) 2020
#  Team hspaces.net
#  Contributors sang.tanhle, HuynhDH
from rest_framework import serializers

from models.media import Media
from models.organization import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    picture_url_info = serializers.SerializerMethodField(method_name='get_picture_url_info')
    cover_url = serializers.SerializerMethodField(method_name='get_cover_url')
    user_info = serializers.SerializerMethodField(method_name='get_user_info')
    type_info = serializers.SerializerMethodField(method_name='get_type_info')
    city_info = serializers.SerializerMethodField(method_name='get_city_info')

    class Meta:
        model = Organization
        exclude = ['user', 'unique_id']

    def get_picture_url_info(self, obj):
        return obj.get_picture_url()

    def get_cover_url(self, obj):
        cover = Media.objects.filter(organization__id=obj.id, set_as_cover=True).first()
        return cover.get_image_url() if cover else None

    def get_user_info(self, obj):
        return {'id': obj.user.id, 'username': obj.user.username, 'email': obj.user.email,
                'picture_url': obj.user.get_picture_url(), 'url': obj.user.url}

    def get_type_info(self, obj):
        return {'id': obj.type.id, 'name': obj.type.name, 'code': obj.type.code}

    def get_city_info(self, obj):
        return {'id': obj.city.id, 'name': obj.city.name} if obj.city else None


class OrganizationOutSerializer(serializers.ModelSerializer):
    picture = serializers.CharField(read_only=True, source='get_picture_url')
    email = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = ['id', 'name', 'email', 'picture', 'url']

    def get_email(self, obj):
        return obj.user.email
