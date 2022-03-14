from datetime import datetime

import cloudinary.api
from rest_framework import serializers

from models.open_innovation import OpenInnovation, ProblemOpenInnovation
from serializers.document_serializer import DocumentOutSerializer


class OpenInnovationSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=0, required=False)
    organization_id = serializers.IntegerField(min_value=0)
    posted_date = serializers.DateField(default=datetime.today, initial=datetime.today,
                                        help_text='Ngày mở open innovation')
    deadline = serializers.DateField(help_text='Ngày kết thúc open innovation')
    tags = serializers.CharField(max_length=128, help_text='Tags giúp tìm kiếm open innovation')
    abstract = serializers.CharField(help_text='Yêu cầu chính của open innovation')
    name = serializers.CharField(max_length=10000, help_text='Tên, tiêu đề thách thức')
    overview = serializers.CharField(help_text='Tổng quan về open innovation')
    detail = serializers.CharField(help_text='Chi tiết về open innovation')
    picture = serializers.FileField(write_only=True)
    picture_url = serializers.URLField(allow_blank=True, allow_null=True, required=False,
                                       help_text='URL của ảnh đại diện của open innovation')
    category = serializers.IntegerField(help_text='Lĩnh vực của open innovation', write_only=True)
    category_name = serializers.CharField(source='category.category_name')
    budget = serializers.DecimalField(max_digits=40, decimal_places=3)
    status = serializers.CharField(max_length=6)
    term_of_use = serializers.CharField()

    def create(self, validated_data):
        organization_id = validated_data.get('organization_id')
        posted_date = validated_data.get('posted_date')
        deadline = validated_data.get('deadline')
        tags = validated_data.get('tags')
        abstract = validated_data.get('abstract')
        name = validated_data.get('abstract')
        overview = validated_data.get('overview')
        detail = validated_data.get('detail')
        picture = validated_data.get('picture')
        category = validated_data.get('category')
        budget = validated_data.get('budget')
        status = validated_data.get('status')
        term_of_use = validated_data.get('term_of_use')
        open_innovation = OpenInnovation.objects.create(organization_id=organization_id, posted_date=posted_date,
                                                        deadline=deadline, tags=tags, abstract=abstract,
                                                        category_id=category, name=name,
                                                        budget=budget, status=status, term_of_use=term_of_use,
                                                        overview=overview, detail=detail, picture=picture)
        return open_innovation

    def update(self, instance, validated_data):
        if instance.picture is not None:
            # delete image before save
            cloudinary.api.delete_resources(instance.picture.public_id)
        instance.posted_date = validated_data.get('posted_date')
        instance.deadline = validated_data.get('deadline')
        instance.tags = validated_data.get('tags')
        instance.abstract = validated_data.get('abstract')
        instance.name = validated_data.get('name')
        instance.overview = validated_data.get('overview')
        instance.detail = validated_data.get('detail')
        instance.picture = validated_data.get('picture')
        instance.category.id = validated_data.get('category')
        instance.budget = validated_data.get('budget')
        instance.status = validated_data.get('status')
        instance.term_of_use = validated_data.get('term_of_use')
        instance.save()
        instance.picture_url = instance.picture.build_url(
            secure=True,
            crop='thumb') if instance.picture is not None else None
        instance.save()
        return instance


class OpenInnovationOutSerializer(serializers.ModelSerializer):
    agent_info = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    documents = serializers.SerializerMethodField()

    class Meta:
        model = OpenInnovation
        fields = '__all__'
        depth = 1

    def get_agent_info(self, obj):
        problem = ProblemOpenInnovation.objects.filter(post=obj).first()
        if not problem:
            return None
        return {'id': problem.agent.id,
                'name': problem.agent.name,
                'picture_url': problem.agent.picture.build_url() if problem.agent.picture else None,
                'url': problem.agent.url}

    def get_images(self, obj):
        return [image.get_image_url() for image in obj.media_set.filter(set_as_cover=False)]

    def get_documents(self, obj):
        return DocumentOutSerializer(obj.document_set.all(), many=True).data
