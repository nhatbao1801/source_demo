from rest_framework import serializers

from models.document import Document, DocumentVersion
from serializers.user_serializer import UserOutSerializer


class DocumentSerializer(serializers.ModelSerializer):
    created_by_info = serializers.SerializerMethodField('get_created_by')
    path_file = serializers.SerializerMethodField('get_full_path_url')
    absolute_path = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = '__all__'
        extra_kwargs = {
            'created_by': {
                'write_only': True
            }

        }

    def get_created_by(self, obj):
        return UserOutSerializer(obj.created_by).data

    def get_full_path_url(self, obj):
        request = self.context.get('request')
        file_url = obj.doc_file
        if not request and file_url:
            return file_url.url
        return request.build_absolute_uri(file_url)

    def get_absolute_path(self, obj):
        if not obj.doc_file:
            return None
        return obj.doc_file.url


class DocumentOutSerializer(serializers.ModelSerializer):
    created_by_info = serializers.SerializerMethodField('get_created_by')
    path_file = serializers.SerializerMethodField('get_full_path_url')
    owner_info = serializers.SerializerMethodField()
    absolute_path = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ['id', 'name', 'description', 'created_by_info', 'path_file', 'owner_info', 'absolute_path']
        depth = 1

    def get_created_by(self, obj):
        return UserOutSerializer(obj.created_by).data

    def get_full_path_url(self, obj):
        request = self.context.get('request')
        file_url = obj.doc_file.url
        if not request:
            return file_url
        return request.build_absolute_uri(file_url)

    def get_absolute_path(self, obj):
        if not obj.doc_file:
            return None
        return obj.doc_file.url

    def get_owner_info(self, obj):
        owner = obj.get_owner
        if owner._meta.model_name == 'openinnovation':
            name = owner.name
        elif owner._meta.model_name == 'openinnovationsubmit':
            name = owner.title
        else:
            name = None
        return {
            "id": owner.id,
            "name": name
        }


class DocumentOutNoneOwnerSerializer(serializers.ModelSerializer):
    created_by_info = serializers.SerializerMethodField('get_created_by')
    path_file = serializers.SerializerMethodField('get_full_path_url')
    absolute_path = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ['id', 'name', 'description', 'created_by_info', 'path_file', 'absolute_path']

    def get_created_by(self, obj):
        return UserOutSerializer(obj.created_by).data

    def get_full_path_url(self, obj):
        request = self.context.get('request')
        file_url = obj.doc_file.url if obj.doc_file else None
        if not file_url:
            return None
        if not request:
            return file_url
        return request.build_absolute_uri(file_url)

    def get_absolute_path(self, obj):
        if not obj.doc_file:
            return None
        return obj.doc_file.url


class DocumentVersionSerializer(serializers.ModelSerializer):
    created_by_info = serializers.SerializerMethodField('get_created_by')
    files_url = serializers.SerializerMethodField('get_full_path_url')

    class Meta:
        model = DocumentVersion
        fields = '__all__'
        extra_kwargs = {
            'created_by': {
                'write_only': True
            }
        }

    def get_created_by(self, obj):
        return UserOutSerializer(obj.created_by).data

    def get_full_path_url(self, obj):
        request = self.context.get('request')
        file_url = obj.doc_file.url
        if not request:
            return file_url
        return request.build_absolute_uri(file_url)
