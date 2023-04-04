from django.contrib import admin
from .models import (
    Post,
    Comment,
)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('body', 'slug', 'created_at', 'updated_at', 'user')
    search_fields = ("slug",)
    list_filter = ('created_at', 'updated_at')
    prepopulated_fields = {"slug": ('body',)}
    raw_id_fields = ("user",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at', 'is_reply', 'updated_at',)
    search_fields = ('body',)
    raw_id_fields = ("user", 'post', 'reply')
    list_filter = ('created_at', 'updated_at', 'is_reply')
