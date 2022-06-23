import requests
from account.serializers.ref_account_serializer import RefAccountSerializerOut
from drf_yasg.utils import swagger_serializer_method
from utils.get_provider_alive.get_provider_alive import get_profile_detail
from event.models.event_participant import EventParticipant
from event.serializers.event_type_serializer import EventTypeSerializerOut
from event.serializers.formality_serializer import FormalitySerializerOut
from event.serializers.privacy_serializer import PrivacySerializerOut
from rest_framework import serializers


class EventParticipantSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventParticipant
        fields = '__all__'

class EventParticipantOut(serializers.ModelSerializer):
    uid_info = serializers.SerializerMethodField('get_uid_info')

    class Meta:
        model = EventParticipant
        fields = ['uid_info']


    @swagger_serializer_method(serializer_or_field=RefAccountSerializerOut)
    def get_uid_info(self, instance):
        if not instance.uid:
            return None
        
        return get_profile_detail(uid=instance.uid)