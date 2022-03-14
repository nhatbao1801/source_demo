from rest_framework import serializers
# from main.models.stage import Stage
from models.stage import Stage

class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = '__all__'
