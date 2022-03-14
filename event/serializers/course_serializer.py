#  Copyright (c) 2020
#  Team hspaces.net
#  Contributors sang.tanhle, HuynhDH

from rest_framework import serializers

from models.course import Course


class CourseSerializer(serializers.Serializer):
    course_category_id = serializers.StringRelatedField()
    skills_accquired = serializers.StringRelatedField(many=True, read_only=True)
    instructors = serializers.StringRelatedField(many=True, read_only=True)
    thumb = serializers.FileField(allow_empty_file=True, allow_null=True, required=False)
    level = serializers.CharField(allow_null=True)
    online_hours = serializers.FloatField(min_value=0, allow_null=True)
    about = serializers.CharField(allow_null=True)
    career_orientation = serializers.CharField(allow_null=True)
    title = serializers.CharField(allow_null=True)
    benefits = serializers.StringRelatedField(many=True, read_only=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class CourseOutSerializer(serializers.ModelSerializer):
    course_category_id_info = serializers.SerializerMethodField()
    course_subcategory_info = serializers.SerializerMethodField()
    creator_info = serializers.SerializerMethodField()
    skills_accquired_info = serializers.SerializerMethodField()
    benefits_info = serializers.SerializerMethodField()
    thumb_url = serializers.SerializerMethodField()
    # users_join_info = serializers.SerializerMethodField()
    # instructors_info = serializers.SerializerMethodField()
    # users_favorite_info = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_course_category_id_info(self, obj):
        return {'id': obj.course_category_id.id,
                'name': obj.course_category_id.name} if obj.course_category_id else None

    def get_course_subcategory_info(self, obj):
        return {'id': obj.course_subcategory.id,
                'name': obj.course_subcategory.name} if obj.course_subcategory else None

    def get_creator_info(self, obj):
        return {'id': obj.creator.id,
                'username': obj.creator.username,
                'email': obj.creator.email,
                'url': obj.creator.url} if obj.creator else None

    def get_skills_accquired_info(self, obj):
        return [{'id': skill.id, 'name': skill.name} for skill in obj.skills_accquired.all()]

    def get_benefits_info(self, obj):
        return [{'id': be.id, 'content': be.content} for be in obj.benefits.all()]

    def get_thumb_url(self, obj):
        return obj.get_thumb_image()

    # def get_users_join_info(self, obj):
    #     return [{'id': user.id,
    #              'username': user.username,
    #              'email': user.email,
    #              'url': user.url} for user in obj.users_join.all()]

    # def get_instructors_info(self, obj):
    #     return [{'id': user.id,
    #              'username': user.username,
    #              'email': user.email,
    #              'url': user.url} for user in obj.instructors.all()]

    # def get_users_favorite_info(self, obj):
    #     return [{'id': user.id,
    #              'username': user.username,
    #              'email': user.email,
    #              'url': user.url} for user in obj.users_favorite.all()]
