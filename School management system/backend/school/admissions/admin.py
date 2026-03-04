from django.contrib import admin
from .models import AdmissionApplication


@admin.register(AdmissionApplication)
class AdmissionApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "grade_applying",
        "email",
        "status",
        "submitted_at",
    )
    list_filter = ("status", "grade_applying")
    search_fields = ("full_name", "email", "phone")
    readonly_fields = ("submitted_at",)
    ordering = ("-submitted_at",)