from rest_framework import serializers
from event.models.stage import Stage


class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = '__all__'
