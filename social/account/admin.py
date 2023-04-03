from django.contrib import admin
from .models import RelationShip


@admin.register(RelationShip)
class RelationShipAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', )
    list_filter = ('created_at',)
