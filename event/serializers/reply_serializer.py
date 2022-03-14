#  Copyright (c) 2020
#  Team hspaces.net
#  Contributors sang.tanhle, HuynhDH

from rest_framework import serializers

from models.reply import Reply


class ReplySerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()

    class Meta:
        model = Reply
        fields = '__all__'
        extra_kwargs = {
            'comment': {'write_only': True},
        }

    def get_user_info(self, inst):
        return {
            'id': inst.user.id,
            'username': inst.user.username,
            'url': inst.user.url,
            'email': inst.user.email,
            'picture': inst.user.picture.build_url() if inst.user.picture is not None else None
        }
