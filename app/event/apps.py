from django.apps import AppConfig
from utils.register_to_registry_service import register_to_registry_service

class EventConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'event'

    def ready(self):
        register_to_registry_service()