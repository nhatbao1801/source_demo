import requests
from datetime import datetime
from account.serializers.ref_account_serializer import RefAccountSerializerOut
from drf_yasg.utils import swagger_serializer_method
from account.models.account import RefAccount
from utils.get_provider_alive.get_provider_alive import get_profile_detail, get_business_level_code_detail, check_user_submited_form
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
    is_owner = serializers.SerializerMethodField('get_is_owner')
    is_joined = serializers.SerializerMethodField('get_is_joined')
    business_level_code = serializers.SerializerMethodField('get_business_level_code')
    out_date = serializers.SerializerMethodField('check_date_out')
    is_form_submited = serializers.SerializerMethodField('check_form_submited')

    class Meta:
        model = Event
        fields = ['id','is_owner', 'is_joined', 'owner_info', 'name', 'cover', 'venue', 'tagline', 'description', 'short_description', 'from_date', 'to_date', 'users_interested_in_info', 'privacy_info', 'co_host_info', 'formality_info', 'event_type_info', 'event_participant_info', 'business_level_code', 'link_online', 'is_form_submited', 'out_date']


    def check_form_submited(self, inst):
        request = None
        if self.context.get('request'):
            request = self.context.get('request')
            uid = request.GET.get('uid')
        if inst.owner != uid:
            return check_user_submited_form(target_id=inst.id, uid=uid)

    def check_date_out(self, inst):
        now = datetime.today().timestamp()
        # format = "%Y-%m-%d %H:%M:%S"
        # inst_to_day = datetime.strptime(str(inst.to_date), format)
        return inst.to_date.timestamp() < now

    def get_business_level_code(self, instance):
        blcode = None
        if not instance.business_level_code:
            return blcode
        return get_business_level_code_detail(bl_code=instance.business_level_code)

    def get_is_owner(self, instance):
        request = None
        if self.context.get('request'):
            request = self.context.get('request')
            uid = request.GET.get('uid')
        if  instance.owner == uid:
            return True
        return False

    def get_is_joined(self, instance):
        request = None
        participants = []
        if self.context.get('request'):
            request = self.context.get('request')
            uid = request.GET.get('uid')
            participants = list(EventParticipant.objects.filter(event_id=instance.id).values_list('uid', flat=True))
        if uid in participants:
            return True
        return False

    @swagger_serializer_method(serializer_or_field=RefAccountSerializerOut)
    def get_ref_account_info(self, instance):
        if not instance.owner:
            return None
        return get_profile_detail(uid=instance.owner)
    
    @swagger_serializer_method(serializer_or_field=RefAccountSerializerOut(many=True))
    def get_co_host_info(self, instance):
        if not instance.co_host:
            return []

        cohost=[]
        for host in instance.co_host.split(','):
            if host:
                cohost.append(get_profile_detail(uid=host))
        return cohost
        # return RefAccountSerializerOut(instance=instance.co_host, many=True).data


    @swagger_serializer_method(serializer_or_field=RefAccountSerializerOut(many=True))
    def get_users_interested_in_info(self, instance):
        if not instance.users_interested_in:
            return []
        
        users_interested=[]
        for user in instance.users_interested_in.split(","):
            users_interested.append(get_profile_detail(uid=user))
        return users_interested


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
        participants = []
        for participant in event_participant:
            participants.append(get_profile_detail(uid=participant))
        return participants
