from django.contrib import admin
from django.utils.html import format_html
from .models import GalleryImage


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("title", "event_name", "image_preview", "uploaded_at")
    list_filter = ("event_name",)
    search_fields = ("title", "event_name")
    readonly_fields = ("uploaded_at", "image_preview")

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="80" style="border-radius:8px;" />',
                obj.image.url,
            )
        return "-"
    
    image_preview.short_description = "Preview"