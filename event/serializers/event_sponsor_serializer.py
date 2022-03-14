from rest_framework import serializers

from event.serializers.event_category_serializer import EventCategorySerializer
from models.sponsor_event import SponsorEvent
from serializers.event_sponsor_serializer import SponsorSerializer


class EventSponsorSerializer(serializers.ModelSerializer):
    sponsor_info = serializers.SerializerMethodField()
    event_category_info = serializers.SerializerMethodField()

    class Meta:
        model = SponsorEvent
        fields = ['id', 'event', 'sponsor', 'event_category', 'custom_category_name', 'sponsor_info', 'event_category_info']

    def get_sponsor_info(self, obj):
        if not obj.sponsor:
            return None
        return SponsorSerializer(obj.sponsor, context={'request': self.context.get('request')}).data

    def get_event_category_info(self, obj):
        if not obj.event_category:
            return None
        return EventCategorySerializer(obj.event_category).data


class EventSponsorOutSerializer(serializers.ModelSerializer):
    sponsor_info = serializers.SerializerMethodField()
    event_category_info = serializers.SerializerMethodField()

    class Meta:
        model = SponsorEvent
        fields = ['id', 'sponsor_info', 'event_category_info']
        depth = 1

    def get_sponsor_info(self, obj):
        if not obj.sponsor:
            return None
        return SponsorSerializer(obj.sponsor, context={'request': self.context.get('request')}).data

    def get_event_category_info(self, obj):
        if not obj.event_category:
            return None
        return EventCategorySerializer(obj.event_category).data
