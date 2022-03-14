from abc import ABC

from django.db.models import Q
from rest_framework import serializers

from event.models.event import Event
from event.serializers.event_sponsor_serializer import EventSponsorOutSerializer


class EventAreaField(serializers.RelatedField, ABC):
    """Custom field for displaying value of area"""

    def to_representation(self, value):
        return value.name


class EventSerializer(serializers.ModelSerializer):
    areas = EventAreaField(many=True, read_only=True)
    is_edit = serializers.SerializerMethodField()
    bought = serializers.SerializerMethodField()
    sponsor_info = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'

    def get_is_edit(self, obj):
        if not obj.get_owner():
            return None
        owner_include_user = obj.get_owner().userexperience_set.values_list('user_id', flat=True)
        request = self.context.get('request')
        if not request:
            return None
        return request.user.id in owner_include_user

    def get_bought(self, obj):
        if self.context and self.context['request']:
            request = self.context.get('request')
            # Danh sách đối tượng đã mua vé sự kiện
            participants = obj.eventparticipant_set.all()
            # Danh sách id đối tượng đã mua vé là user
            ids_user_participant = participants.filter(user__isnull=False).values_list('user_id', flat=True)
            # Danh sách id đối tượng đã mua vé là team
            ids_team_participant = participants.filter(team__isnull=False).values_list('team_id', flat=True)
            # Danh sách id team mà user hiện tại đang làm việc
            ids_team_working = request.user.userexperience_set.filter(team__isnull=False).values_list('team_id',
                                                                                                      flat=True)
            # Kiểm tra user hiện tại | team của user hiện tại đã mua vé hay chưa
            if request.user.id not in ids_user_participant and len(
                    set(ids_team_participant) & set(ids_team_working)) == 0:
                return False
            return True
        return None

    def get_sponsor_info(self, obj):
        if not obj.sponsorevent_set.all():
            return []
        return EventSponsorOutSerializer(obj.sponsorevent_set.all(), many=True, context={'request': self.context.get('request')}).data


class EventOutSerializer(serializers.ModelSerializer):
    # picture = serializers.CharField(read_only=True, source='get_picture_url')
    # areas_info = serializers.SerializerMethodField()
    # city_info = serializers.SerializerMethodField()
    # type_info = serializers.SerializerMethodField()
    # object_creation = serializers.SerializerMethodField()
    # areas_id = serializers.SerializerMethodField()
    # city_id = serializers.SerializerMethodField()
    # event_type_id = serializers.SerializerMethodField()
    # cover = serializers.SerializerMethodField()
    # is_edit = serializers.SerializerMethodField()
    # ticket_info = serializers.SerializerMethodField()
    # participants = serializers.SerializerMethodField()
    # bought = serializers.SerializerMethodField()
    # sponsor_info = serializers.SerializerMethodField()
    # application_info = serializers.SerializerMethodField()
    # application_form_info = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'
        depth = 1

    def get_areas_info(self, obj):
        return [{"id": area.id, "name": area.name} for area in obj.areas.all()]

    def get_areas_id(self, obj):
        areas_id = []
        for ar_id in obj.areas.all():
            areas_id.append(ar_id.id)
        return areas_id

    def get_type_info(self, obj):
        if not obj.type:
            return None
        return {"id": obj.type.id, "name": obj.type.name}

    def get_event_type_id(self, obj):
        if not obj.type:
            return None
        return obj.type.id

    def get_city_info(self, obj):
        if not obj.city:
            return None
        return {"id": obj.city.id, "name": obj.city.name}

    def get_city_id(self, obj):
        if not obj.city:
            return None
        return obj.city.id

    def get_is_edit(self, obj):
        if not obj.get_owner():
            return None
        owner = obj.get_owner()
        owner_include_user = owner.userexperience_set.all().values_list('user_id', flat=True)
        request = self.context.get('request')
        if not request:
            return None
        return request.user.id in owner_include_user

    def get_object_creation(self, obj):
        owner = obj.get_owner()
        if not owner:
            return None
        return {
            'name': owner.name,
            'picture': owner.get_picture_url(),
            'url': owner.url
        }

    def get_cover(self, obj):
        media = obj.media_set.filter(Q(media_type='img') & Q(set_as_cover=True)).last()
        cover_picture = None
        if media and media.image:
            cover_picture = media.image.build_url(secure=True)
        return cover_picture

    def get_ticket_info(self, obj):
        if not obj.ticket_set.all():
            return []
        return TicketOutSerializer(obj.ticket_set.all(), many=True).data

    def get_participants(self, obj):
        pass
        event_user_participants = []
        event_team_participants = []
        if obj.eventparticipant_set.all().filter(team__isnull=True):
            event_user_participants = UserOutSerializer(User.objects.filter(
                pk__in=obj.eventparticipant_set.all().filter(team__isnull=True).values_list('user_id', flat=True)),
                many=True).data
        if obj.eventparticipant_set.all().filter(user__isnull=True):
            event_team_participants = TeamOutSerializer(Team.objects.filter(
                pk__in=obj.eventparticipant_set.all().filter(user__isnull=True).values_list('team_id', flat=True)),
                many=True).data
        return {"users": event_user_participants, "teams": event_team_participants}

    def get_bought(self, obj):
        """ if self.context.get('request'):
            request = self.context.get('request')
            # Danh sách đối tượng đã mua vé sự kiện
            participants = obj.eventparticipant_set.all()
            # Danh sách id đối tượng đã mua vé là user
            ids_user_participant = participants.filter(user__isnull=False).values_list('user_id', flat=True)
            # Danh sách id đối tượng đã mua vé là team
            ids_team_participant = participants.filter(team__isnull=False).values_list('team_id', flat=True)
            # Danh sách id team mà user hiện tại đang làm việc
            ids_team_working = request.user.userexperience_set.filter(team__isnull=False).values_list('team_id',
                                                                                                      flat=True)
            # Kiểm tra user hiện tại | team của user hiện tại đã mua vé hay chưa
            if request.user.id not in ids_user_participant and len(
                    set(ids_team_participant) & set(ids_team_working)) == 0:
                return False
            return True
        return None """
        pass

    def get_sponsor_info(self, obj):
        if not obj.sponsorevent_set.all():
            return []
        return EventSponsorOutSerializer(obj.sponsorevent_set.all(), many=True, context={'request': self.context.get('request')}).data

    def get_application_info(self, obj):
        pass
        """ try:
            return ApplicationSerializer(obj.application).data
        except:
            return None """

    def get_application_form_info(self, obj):
        pass
        # try:
        #     af_info = obj.application.applicationform_set.all().filter(is_used=True).first()
        #     if not af_info:
        #         return None
        #     return ApplicationFormOutSerializer(af_info).data
        # except Exception as e:
        #     print(e)
        #     return None


class EventSerializerForValidation(serializers.Serializer):
    """Used for validation only"""
    event_id = serializers.IntegerField(min_value=0)
    city_id = serializers.IntegerField(min_value=0)
    areas_id = serializers.CharField()
    event_type_id = serializers.IntegerField(min_value=0)
    name = serializers.CharField()
    hash_tag = serializers.CharField()
    street_address = serializers.CharField()
    url = serializers.CharField()
    venue = serializers.CharField()
    tagline = serializers.CharField()
    description = serializers.CharField()
    from_date = serializers.DateTimeField()
    to_date = serializers.DateTimeField()
    schedule = serializers.CharField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
