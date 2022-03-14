from rest_framework import serializers

from models.ticket import Ticket


class TicketSerializer(serializers.ModelSerializer):
    event_info = serializers.SerializerMethodField()
    timezone_info = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = '__all__'

    def get_event_info(self, obj):
        return {"id": obj.event.id, "name": obj.event.name, "picture": obj.event.get_picture_url()}

    def get_timezone_info(self, obj):
        if not obj.timezone:
            return {}
        return {"id": obj.timezone.id, "value": obj.timezone.value, "text": obj.timezone.text, "gmt": obj.timezone.gmt}


class TicketOutSerializer(serializers.ModelSerializer):
    timezone_info = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ['id', 'timezone_info', 'name', 'description', 'sale_from', 'sale_to', 'max_quantity', 'sold', 'price']

    def get_timezone_info(self, obj):
        if not obj.timezone:
            return {}
        return {"id": obj.timezone.id, "value": obj.timezone.value, "text": obj.timezone.text, "gmt": obj.timezone.gmt}
