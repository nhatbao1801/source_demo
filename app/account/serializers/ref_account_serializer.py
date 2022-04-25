from account.models.account import RefAccount
from rest_framework import serializers


class RefAccountSerializerIn(serializers.ModelSerializer):

    class Meta:
        model = RefAccount
        fields = '__all__'


class RefAccountSerializerOut(serializers.ModelSerializer):
    class Meta:
        model = RefAccount
        fields = ['id', 'user_id', 'full_name']


class EventParcitipantSerializerInfo(serializers.ModelSerializer):
    class Meta:
        model = RefAccount
        fields = ['id', 'user_id', 'full_name', 'email']
