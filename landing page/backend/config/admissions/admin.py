from django.contrib import admin
from .models import Admission


@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):

    list_display = (
        "student_name",
        "father_name",
        "grade",
        "status",
        "created_at",
    )

    search_fields = (
        "student_name",
        "father_name",
        "email",
    )

    list_filter = (
        "grade",
        "status",
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
    )