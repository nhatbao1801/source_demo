from rest_framework import serializers

from event.serializers.event_serializer import EventOutSerializer
from models import EventParticipant
from main.serializers.user_serializer import UserOutSerializer
from startup.serializers.team_serializer import TeamOutSerializer


class EventParticipantSerializer(serializers.ModelSerializer):
    event_info = serializers.SerializerMethodField()
    user_info = serializers.SerializerMethodField()
    team_info = serializers.SerializerMethodField()

    class Meta:
        model = EventParticipant
        fields = '__all__'
        extra_kwargs = {
            'event': {'write_only': True},
            'user': {'write_only': True},
            'team': {'write_only': True}
        }

    def get_event_info(self, obj):
        if not obj.event:
            return None
        return EventOutSerializer(obj.event).data

    def get_user_info(self, obj):
        if not obj.user:
            return None
        return UserOutSerializer(obj.user).data

    def get_team_info(self, obj):
        if not obj.team:
            return None
        return TeamOutSerializer(obj.team).data


class EventOutParticipantSerializer(serializers.ModelSerializer):
    event_info = serializers.SerializerMethodField()
    user_info = serializers.SerializerMethodField()
    team_info = serializers.SerializerMethodField()

    class Meta:
        model = EventParticipant
        fields = ['id', 'event_info', 'user_info', 'team_info']

    def get_event_info(self, obj):
        if not obj.event:
            return None
        return EventOutSerializer(obj.event).data

    def get_user_info(self, obj):
        if not obj.user:
            return None
        return UserOutSerializer(obj.user).data

    def get_team_info(self, obj):
        if not obj.team:
            return None
        return TeamOutSerializer(obj.team).data
