from django.contrib import admin
from .models import Gallery


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "category",
        "uploaded_at",
    )

    search_fields = (
        "title",
        "category",
    )

    list_filter = (
        "category",
        "uploaded_at",
    )

    ordering = (
        "-uploaded_at",
    )

    readonly_fields = (
        "uploaded_at",
    )