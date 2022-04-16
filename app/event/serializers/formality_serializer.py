from event.models.formality import Formality
from rest_framework import serializers


class FormalitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Formality
        fields = '__all__'

class FormalitySerializerOut(serializers.ModelSerializer):

    class Meta:
        model = Formality
        fields = ['code', 'name']
