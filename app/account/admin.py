from django.contrib import admin

from .models import RefAccount

# Register your models here.
class RefAccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'full_name')
admin.site.register(RefAccount, RefAccountAdmin)