from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Event)
admin.site.register(EventParticipant)
admin.site.register(EventType)
admin.site.register(Privacy)
admin.site.register(Formality)
