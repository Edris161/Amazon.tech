from django.contrib import admin
from django.utils.html import format_html
from .models import SiteSetting


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ("school_name", "logo_preview", "email", "phone")
    readonly_fields = ("logo_preview",)

    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" width="100" style="border-radius:6px;" />',
                obj.logo.url,
            )
        return "-"
    
    logo_preview.short_description = "Logo"