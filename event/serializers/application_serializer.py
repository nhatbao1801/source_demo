from rest_framework import serializers

from models.application import Application, ApplicationForm, ApplicationFormAnswer
from serializers.contest_serializer import ContestOutSerializer
from serializers.organization_serializer import OrganizationSerializer
from serializers.user_serializer import UserOutSerializer
from startup.serializers.team_serializer import TeamOutSerializer


class ApplicationSerializer(serializers.ModelSerializer):
    # contest_info = serializers.SerializerMethodField()
    # job_info = serializers.SerializerMethodField()
    # job_freelance_info = serializers.SerializerMethodField()
    # incubator_info = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = '__all__'

    # def get_job_info(self, obj):
    #     try:
    #         j = obj.job
    #         if not j:
    #             return None
    #         return JobSerializer(j).data
    #     except ObjectDoesNotExist:
    #         return None
    #
    # def get_job_freelance_info(self, obj):
    #     try:
    #         f = obj.incubator
    #         if not f:
    #             return None
    #         return JobFreelanceSerializer(f).data
    #     except ObjectDoesNotExist:
    #         return None
    #
    # def get_incubator_info(self, obj):
    #     try:
    #         i = obj.incubator
    #         if not i:
    #             return None
    #         return IncubatorSerializer(i).data
    #     except ObjectDoesNotExist:
    #         return None


class ApplicationOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'


class ApplicationFormSerializer(serializers.ModelSerializer):
    users_answers_info = serializers.SerializerMethodField()

    class Meta:
        model = ApplicationForm
        fields = '__all__'

    def get_users_answers_info(self, obj):
        application_form_answer = obj.applicationformanswer_set.all()
        return ApplicationFormAnswerOutSerializer(application_form_answer, many=True).data


class ApplicationFormOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationForm
        fields = ['id', 'schema', 'is_used', 'form_data', 'ui_schema']


class ApplicationFormAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationFormAnswer
        fields = '__all__'


class ApplicationFormAnswerOutSerializer(serializers.ModelSerializer):
    owner_answer = serializers.SerializerMethodField()
    owner_answer_type = serializers.SerializerMethodField()

    class Meta:
        model = ApplicationFormAnswer
        fields = ['id', 'owner_answer', 'form_data_answer', 'owner_answer_type']

    def get_owner_answer(self, obj):
        if obj.user_id:
            return UserOutSerializer(obj.get_owner).data
        if obj.team_id:
            return TeamOutSerializer(obj.get_owner).data
        if obj.organization_id:
            return OrganizationSerializer(obj.get_owner).data
        if obj.contest_id:
            return ContestOutSerializer(obj.get_owner).data

    def get_owner_answer_type(self, obj):
        if obj.user_id:
            return 'user'
        if obj.team_id:
            return 'team'
        if obj.organization_id:
            return 'organization'
        if obj.contest_id:
            return 'contest'
