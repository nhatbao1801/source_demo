from rest_framework import serializers

from models.post import Post
from serializers.comment_serializer import CommentSerializer


class PostSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(method_name='get_images')
    comments = serializers.SerializerMethodField(method_name='get_comments')
    heaters = serializers.SerializerMethodField(method_name='get_heaters')
    user_info = serializers.SerializerMethodField(method_name='get_user_info')
    privacy_setting_info = serializers.SerializerMethodField(method_name='get_privacy_setting_info')
    owner_permission = serializers.SerializerMethodField(method_name='get_owner_permission')

    class Meta:
        model = Post
        fields = '__all__'
        # extra_kwargs = {
        #     'user': {'write_only': True},
        #     'team': {'write_only': True},
        #     'organization': {'write_only': True},
        #     'contest': {'write_only': True},
        #     'event': {'write_only': True},
        #     'deal': {'write_only': True}
        # }

    def get_images(self, obj):
        return [img.get_image_url() for img in obj.media_set.all()]

    def get_comments(self, obj):
        return CommentSerializer(obj.comment_set.all(), many=True).data

    def get_heaters(self, obj):
        return [{"id": heat.id,
                 "user_id": heat.user.id,
                 "user_name": heat.user.username,
                 "user_avatar": heat.user.get_picture_url(),
                 "url": heat.user.url} for heat in obj.heat_set.all()]

    def get_user_info(self, obj):
        return {"id": obj.user.id,
                "username": obj.user.username,
                "user_picture": obj.user.get_picture_url(),
                "user_url": obj.user.url}

    def get_privacy_setting_info(self, obj):
        return {"id": obj.privacy_setting.id, "name": obj.privacy_setting.name, "code": obj.privacy_setting.code}

    def get_owner_permission(self, obj):
        if self.context.get('request'):
            if self.context.get('request').user.id != obj.user.id:
                return False
            return True
        return None