from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from models.event import Event


# @registry.register_document
class EventDocument(Document):
    picture = fields.TextField(attr='get_picture_url')

    class Index:
        name = 'events'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Event
        fields = [
            'id',
            'name',
            'url',
            'tagline'
        ]
