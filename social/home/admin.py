from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('body', 'slug', 'created_at', 'updated_at', 'user')
    search_fields = ("slug",)
    list_filter = ('created_at', 'updated_at')
    prepopulated_fields = {"slug": ('body',)}
    raw_id_fields = ("user", )
