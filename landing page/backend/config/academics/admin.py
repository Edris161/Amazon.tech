from django.contrib import admin
from .models import Academics


@admin.register(Academics)
class AcademicsAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "grade_level",
        "duration",
        "created_at",
    )

    search_fields = (
        "title",
        "grade_level",
    )

    list_filter = (
        "grade_level",
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
    )