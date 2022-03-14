from rest_framework import serializers

from models.sponsor import Sponsor


class SponsorSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()

    class Meta:
        model = Sponsor
        fields = ['id', 'logo', 'name', 'is_verified', 'logo_url']

    def get_logo_url(self, obj):
        request = self.context.get('request')
        file_url = obj.logo.url
        if not request:
            return file_url
        return request.build_absolute_uri(file_url)
