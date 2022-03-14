from rest_framework import serializers

from models.fund_raising import FundRaising


class FundRaisingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundRaising
        fields = '__all__'