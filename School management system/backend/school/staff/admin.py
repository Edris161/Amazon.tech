from django.contrib import admin
from django.utils.html import format_html
from .models import Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "subject",
        "is_active",
        "display_order",
        "photo_preview",
    )
    list_filter = ("is_active", "subject")
    search_fields = ("first_name", "last_name", "subject")
    ordering = ("display_order",)
    readonly_fields = ("created_at", "photo_preview")

    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" width="60" style="border-radius:50%;" />',
                obj.photo.url,
            )
        return "-"
    
    photo_preview.short_description = "Photo"