from rest_framework import serializers
from event.models.team import Team
from event.serializers.stage_serializer import StageSerializer
from event.serializers.user_serializer import UserOutSerializer


class TeamSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=0, required=False)
    user_id = serializers.IntegerField(min_value=0, help_text='Admin của trang', write_only=True)
    stage_id = serializers.IntegerField(min_value=0, write_only=True)
    name = serializers.CharField(max_length=255)
    picture = serializers.FileField(write_only=True)
    picture_url = serializers.URLField(allow_blank=True, allow_null=True, required=False)
    url = serializers.CharField(max_length=300, allow_null=True, allow_blank=True, required=False)
    founded_date = serializers.DateTimeField()
    tagline = serializers.CharField(max_length=100)
    android_app_link = serializers.URLField(max_length=300, allow_null=True, allow_blank=True)
    ios_app_link = serializers.URLField(max_length=300, allow_null=True, allow_blank=True)
    description = serializers.CharField(max_length=2500)
    is_startup = serializers.BooleanField(default=False)
    vision = serializers.CharField(allow_null=True, allow_blank=True)
    mission = serializers.CharField(allow_null=True, allow_blank=True)
    core_value = serializers.CharField(allow_null=True, allow_blank=True)
    phone_num = serializers.CharField(max_length=12, required=False)
    street_address = serializers.CharField(max_length=512, allow_blank=True)

    owner_info = serializers.SerializerMethodField()
    stage_info = serializers.SerializerMethodField()

    def create(self, validated_data):
        user_id = validated_data.get('user_id')
        stage_id = validated_data.get('stage_id')
        name = validated_data.get('name')
        picture = validated_data.get('picture')
        founded_date = validated_data.get('founded_date')
        tagline = validated_data.get('tagline')
        android_app_link = validated_data.get('android_app_link')
        ios_app_link = validated_data.get('ios_app_link')
        description = validated_data.get('description')
        is_startup = validated_data.get('is_startup')
        vision = validated_data.get('vision')
        mission = validated_data.get('mission')
        core_value = validated_data.get('core_value')
        phone_num = validated_data.get('phone_num')
        street_address = validated_data.get('street_address')

        team = Team.objects.create(user_id=user_id, stage_id=stage_id, name=name, picture=picture,
                                   founded_date=founded_date, tagline=tagline, android_app_link=android_app_link,
                                   ios_app_link=ios_app_link, description=description, is_startup=is_startup,
                                   vision=vision, mission=mission, core_value=core_value, phone_num=phone_num,
                                   street_address=street_address)
        return team

    def get_owner_info(self, obj):
        return UserOutSerializer(obj.user).data

    def get_stage_info(self, obj):
        return StageSerializer(obj.stage).data


class TeamOutSerializer(serializers.ModelSerializer):
    picture = serializers.CharField(read_only=True, source='get_picture_url')
    email = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ['id', 'name', 'email', 'picture', 'url']

    def get_email(self, obj):
        return obj.user.email
