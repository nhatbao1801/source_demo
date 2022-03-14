#  Copyright (c) 2020.
#  Team hspaces.net
#  Contributors sang.tanhle, HuynhDH
from django.db.models import Q
from rest_framework import serializers

from models.contest import Contest
from models.contest_participant import ContestParticipant
from models.funding import Funding
from fundraising_serializer import FundRaisingSerializer


class ContestSerializer(serializers.ModelSerializer):
    # organization = serializers.StringRelatedField(many=False)
    # city = serializers.StringRelatedField(many=False)
    is_edit = serializers.SerializerMethodField()
    application_info = serializers.SerializerMethodField()

    class Meta:
        model = Contest
        fields = '__all__'

    def get_is_edit(self, obj):
        if not obj.organization:
            return None
        owner_include_user = obj.organization.userexperience_set.values_list('user_id', flat=True)
        request = self.context.get('request')
        if not request:
            return None
        return request.user.id in owner_include_user

    def get_application_info(self, obj):
        try:
            app = obj.application
            if app:
                timezone = None
                if app.timezone:
                    timezone = {
                        "id": app.timezone.id,
                        "gmt": app.timezone.gmt,
                        "value": app.timezone.value,
                        "text": app.timezone.text,
                    }
                app_info = {
                    'id': app.id,
                    'contest': app.contest.title if app.contest else None,
                    'job': app.job.title if app.job else None,
                    'job_freelance': app.job_freelance.title if app.job_freelance else None,
                    'incubator': app.incubator.name if app.incubator else None,
                    'event': app.event.name if app.event else None,
                    'organization': app.organization.name if app.organization else None,
                    'accept_type': app.accept_type,
                    'apply_from': str(app.apply_from),
                    'apply_to': str(app.apply_to),
                    'run_from': str(app.run_from),
                    'run_to': str(app.run_to),
                    'app': app.hide_score,
                    'timezone': timezone
                }
                return app_info
            # return ApplicationOutSerializer(obj.application).data
        except:
            return None


class ContestOutSerializer(serializers.ModelSerializer):
    organization_info = serializers.SerializerMethodField()
    city_info = serializers.SerializerMethodField()
    picture = serializers.CharField(read_only=True, source='get_picture_url')
    is_edit = serializers.SerializerMethodField()
    application_info = serializers.SerializerMethodField()
    cover_picture = serializers.SerializerMethodField(method_name='get_cover_picture')
    status_user_current = serializers.SerializerMethodField(method_name='get_status_user_current')
    is_been_invested = serializers.SerializerMethodField(method_name='get_is_been_invested')
    application_form_info = serializers.SerializerMethodField()
    has_fundraising = serializers.SerializerMethodField()
    has_funding = serializers.SerializerMethodField()
    fundraising_info = serializers.SerializerMethodField()

    class Meta:
        model = Contest
        fields = '__all__'

    def get__picture(self, obj):
        return obj.get_picture_url()

    def get_organization_info(self, obj):
        return {
            "id": obj.organization.id,
            "name": obj.organization.name,
            "picture_url": obj.organization.get_picture_url(),
            "url": obj.organization.url
        }

    def get_city_info(self, obj):
        if not obj.city:
            return None
        return {
            "id": obj.city.id,
            "name": obj.city.name
        }

    def get_is_edit(self, obj):
        if not obj.organization:
            return None
        owner_include_user = obj.organization.userexperience_set.values_list('user_id', flat=True)
        request = self.context.get('request') if self.context and self.context['request'] else None
        if not request:
            return None
        return request.user.id in owner_include_user

    def get_application_info(self, obj):
        try:
            app = obj.application
            if app:
                timezone = None
                if app.timezone:
                    timezone = {
                        "id": app.timezone.id,
                        "gmt": app.timezone.gmt,
                        "value": app.timezone.value,
                        "text": app.timezone.text,
                    }
                app_info = {
                    'id': app.id,
                    'contest': app.contest.title if app.contest else None,
                    'job': app.job.title if app.job else None,
                    'job_freelance': app.job_freelance.title if app.job_freelance else None,
                    'incubator': app.incubator.name if app.incubator else None,
                    'event': app.event.name if app.event else None,
                    'organization': app.organization.name if app.organization else None,
                    'accept_type': app.accept_type,
                    'apply_from': str(app.apply_from),
                    'apply_to': str(app.apply_to),
                    'run_from': str(app.run_from),
                    'run_to': str(app.run_to),
                    'app': app.hide_score,
                    'timezone': timezone
                }
                return app_info
        except:
            return None

    def get_cover_picture(self, obj):
        return obj.media_set.first().get_image_url() if obj.media_set.first() else None

    def get_status_user_current(self, obj):
        if self.context and self.context['request']:
            id_user_current = self.context.get('request').user.id
            if id_user_current in obj.organization.userexperience_set.values_list('user_id', flat=True):
                return "ADMIN"
            contest_participant = ContestParticipant.objects.filter(
                contest__id=obj.id).filter(Q(user__id=id_user_current) | Q(team__user__id=id_user_current)).first()
            if contest_participant is None:
                return "NOT_YET_REQUEST"
            if contest_participant.status is None:
                return "PENDING"
            if contest_participant.status is True:
                return "JOINED"
            if contest_participant.status is False:
                return "DENIED"
        return None

    def get_is_been_invested(self, obj):
        _is_obj = None
        try:
            _is_obj = obj.funding
            return True
        except:
            return False

    def get_application_form_info(self, obj):
        try:
            af_info = obj.application.applicationform_set.all().filter(is_used=True).first()
            if not af_info:
                return None
            return {
                'id': af_info.id, 'schema': af_info.schema, 'is_used': af_info.is_used, 'form_data': af_info.form_data,
                'ui_schema': af_info.ui_schema
            }
        except Exception as e:
            print(e)
            return None

    def get_has_fundraising(self, obj):
        try:
            is_fundraising = obj.fundraising
            return True
        except:
            return False

    def get_has_funding(self, obj):
        if self.context and self.context['request']:
            user = self.context.get('request').user
            funding_of_user = Funding.objects.filter(organization__user__id=user.id)
            if funding_of_user:
                return True
            return False
        return None

    def get_fundraising_info(self, obj):
        try:
            return FundRaisingSerializer(obj.fundraising).data
        except:
            return False
