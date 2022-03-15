#  Copyright (c) 2020
#  Team hspaces.net
#  Contributors sang.tanhle, HuynhDH

from rest_framework import serializers

from event.models.user import User


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    picture = serializers.SerializerMethodField(method_name='build_picture_url')
    last_login: serializers.DateTimeField()
    is_superuser: serializers.BooleanField(read_only=True)
    first_name: serializers.StringRelatedField()
    last_name: serializers.StringRelatedField()
    is_staff: serializers.BooleanField()
    is_active: serializers.BooleanField()
    date_joined: serializers.DateTimeField()
    username: serializers.StringRelatedField()
    email: serializers.EmailField()
    picture_url: serializers.StringRelatedField()
    short_bio: serializers.StringRelatedField()
    url: serializers.StringRelatedField()
    something_great_to_tell: serializers.StringRelatedField()
    gender: serializers.StringRelatedField()
    phone_num: serializers.StringRelatedField()
    last_modified: serializers.DateTimeField()
    setting: serializers.StringRelatedField()
    city: serializers.StringRelatedField()
    content: serializers.StringRelatedField()
    status: serializers.StringRelatedField()
    datetime_sent: serializers.DateTimeField()

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def build_picture_url(self, obj):
        if not obj.picture:
            return None
        return obj.picture.build_url(width=200, height=200, secure=True, crop='thumb')


class UserOutSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    picture = serializers.SerializerMethodField(method_name='build_picture_url')
    first_name: serializers.StringRelatedField()
    last_name: serializers.StringRelatedField()
    username: serializers.StringRelatedField()
    email: serializers.EmailField()
    url: serializers.StringRelatedField()

    class Meta:
        model = User
        fields = ('id', 'picture', 'first_name', 'last_name', 'username', 'email', 'url')

    def build_picture_url(self, obj):
        if not obj.picture:
            return None
        return obj.picture.build_url(width=200, height=200, secure=True, crop='thumb')
