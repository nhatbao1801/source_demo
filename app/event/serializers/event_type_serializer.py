from event.models.event_type import EventType
from rest_framework import serializers


class EventTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventType
        fields = '__all__'

class EventTypeSerializerOut(serializers.ModelSerializer):

    class Meta:
        model = EventType
        fields = ['id', 'code', 'name']