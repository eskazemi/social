from django.contrib import admin
from .models import (
    RelationShip,
    Profile,
)
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class UserAdminExtend(UserAdmin):
    inlines = (ProfileInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdminExtend)


@admin.register(RelationShip)
class RelationShipAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user',)
    list_filter = ('created_at',)
