from django.contrib import admin
from .models import Media


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('company', 'media_type')
    list_filter = ('media_type', 'company')