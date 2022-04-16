from event.models.privacy import Privacy
from rest_framework import serializers


class PrivacySerializer(serializers.ModelSerializer):

    class Meta:
        model = Privacy
        fields = '__all__'


class PrivacySerializerOut(serializers.ModelSerializer):

    class Meta:
        model = Privacy
        fields = ['id', 'code', 'name']
