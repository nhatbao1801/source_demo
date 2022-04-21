from account.serializers.ref_account_serializer import RefAccountSerializerOut
from drf_yasg.utils import swagger_serializer_method
from event.models.event_participant import EventParticipant
from event.serializers.event_participant_serializer import EventParticipantOut
from event.models.event import Event
from event.serializers.event_type_serializer import EventTypeSerializerOut
from event.serializers.formality_serializer import FormalitySerializerOut
from event.serializers.privacy_serializer import PrivacySerializerOut
from rest_framework import serializers


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'

class EventSerializerOut(serializers.ModelSerializer):
    owner_info = serializers.SerializerMethodField('get_ref_account_info')
    users_interested_in_info = serializers.SerializerMethodField('get_users_interested_in_info')
    co_host_info = serializers.SerializerMethodField('get_co_host_info')
    privacy_info = serializers.SerializerMethodField('get_privacy_info')
    formality_info = serializers.SerializerMethodField('get_formality_info')
    event_type_info = serializers.SerializerMethodField('get_event_type_info')
    event_participant_info = serializers.SerializerMethodField('get_event_participant_info')

    class Meta:
        model = Event
        fields = ['id', 'owner_info', 'name', 'cover', 'venue', 'tagline', 'description', 'from_date', 'to_date', 'users_interested_in_info', 'privacy_info', 'co_host_info', 'formality_info', 'event_type_info', 'event_participant_info']


    @swagger_serializer_method(serializer_or_field=RefAccountSerializerOut)
    def get_ref_account_info(self, instance):
        if not instance.owner:
            return None
        return RefAccountSerializerOut(instance=instance.owner).data
    
    @swagger_serializer_method(serializer_or_field=RefAccountSerializerOut(many=True))
    def get_co_host_info(self, instance):
        if not instance.co_host:
            return []
        return RefAccountSerializerOut(instance=instance.co_host, many=True).data


    @swagger_serializer_method(serializer_or_field=RefAccountSerializerOut(many=True))
    def get_users_interested_in_info(self, instance):
        if not instance.users_interested_in:
            return []
        return RefAccountSerializerOut(instance=instance.users_interested_in, many=True).data

    @swagger_serializer_method(serializer_or_field=PrivacySerializerOut)
    def get_privacy_info(self, instance):
        if not instance.privacy:
            return None
        return PrivacySerializerOut(instance=instance.privacy).data

    @swagger_serializer_method(serializer_or_field=FormalitySerializerOut)
    def get_formality_info(self, instance):
        if not instance.formality:
            return None
        return FormalitySerializerOut(instance=instance.formality).data
    
    @swagger_serializer_method(serializer_or_field=EventTypeSerializerOut)
    def get_event_type_info(self, instance):
        if not instance.event_type:
            return None
        return EventTypeSerializerOut(instance=instance.event_type).data


    @swagger_serializer_method(serializer_or_field=RefAccountSerializerOut)
    def get_event_participant_info(self, instance):
        event_participant = list(EventParticipant.objects.filter(event_id=instance.id).values_list('uid', flat=True))
        # return RefAccountSerializerOut(instance=event_participant, many=True).data
        return {
            "data": event_participant
        }

    