from django.contrib import admin
from .models import Staff


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "position",
        "email",
        "phone",
        "created_at",
    )

    search_fields = (
        "name",
        "position",
        "email",
    )

    list_filter = (
        "position",
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
    )