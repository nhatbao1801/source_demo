import json
from abc import ABC

from rest_framework import serializers

# from .models.area import Area
# from .models.idea import Idea
from event.models.area import Area
from event.models.idea import Idea

class TechnologyListingField(serializers.RelatedField, ABC):

    def to_representation(self, value):
        return {'id': value.id, 'name': value.name}


class TeamField(serializers.RelatedField, ABC):

    def to_representation(self, value):
        return {'id': value.id, 'name': value.name}


class IdeaSerializer(serializers.ModelSerializer):
    team = TeamField(many=False, read_only=True)
    technologies = TechnologyListingField(many=True, read_only=True)

    team_id = serializers.CharField(help_text='Team id', write_only=True)
    technologies_id = serializers.CharField(help_text='List of area_id "[1,2,3]"', write_only=True)

    class Meta:
        model = Idea
        fields = '__all__'
        extra_kwargs = {
            'describe': {
                'help_text': 'Describe an idea'
            },
            'title': {
                'help_text': 'Title of an idea'
            }
        }

    def create(self, validated_data):
        team_id = validated_data.get('team_id')
        technologies_id = validated_data.get('technologies_id')
        title = validated_data.get('title')
        describe = validated_data.get('describe')
        # Create idea first
        idea = None
        try:
            areas_id = json.loads(technologies_id)
            if not isinstance(areas_id, list):
                raise ValueError('technologies_id must be a list of area_id')
            idea = Idea.objects.create(team_id=team_id, title=title, describe=describe)
            for area_id in areas_id:
                idea.technologies.add(Area.objects.get(id=area_id))
        except (ValueError, Exception) as e:
            raise e
        return idea

    def update(self, instance, validated_data):
        instance.team_id = validated_data.get('team_id')
        instance.title = validated_data.get('title')
        instance.describe = validated_data.get('describe')
        technologies_id = validated_data.get('technologies_id')
        try:
            areas_id = json.loads(technologies_id)
            if not isinstance(areas_id, list):
                raise ValueError('technologies_id must be a list of area_id')
            instance.technologies.clear()
            for area_id in areas_id:
                instance.technologies.add(Area.objects.get(id=area_id))
        except (ValueError, Exception) as e:
            raise e
        instance.save()
        return instance
