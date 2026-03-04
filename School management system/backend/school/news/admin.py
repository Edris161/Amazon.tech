from django.contrib import admin
from django.utils.html import format_html
from .models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "is_published",
        "published_at",
        "image_preview",
        "created_at",
    )
    list_filter = ("is_published", "published_at")
    search_fields = ("title", "excerpt")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("-published_at",)
    readonly_fields = ("created_at", "updated_at", "image_preview")

    def image_preview(self, obj):
        if obj.featured_image:
            return format_html(
                '<img src="{}" width="80" style="border-radius:6px;" />',
                obj.featured_image.url,
            )
        return "-"
    
    image_preview.short_description = "Preview"