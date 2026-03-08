from django.contrib import admin
from .models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "slug",
        "published_at",
    )

    search_fields = (
        "title",
        "short_description",
    )

    list_filter = (
        "published_at",
    )

    ordering = (
        "-published_at",
    )

    readonly_fields = (
        "slug",
        "published_at",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }