from account.models.account import RefAccount
from rest_framework import serializers


class RefAccountSerializerIn(serializers.ModelSerializer):

    class Meta:
        model = RefAccount
        fields = '__all__'


class RefAccountSerializerOut(serializers.ModelSerializer):
    class Meta:
        model = RefAccount
        fields = ['id', 'full_name']
