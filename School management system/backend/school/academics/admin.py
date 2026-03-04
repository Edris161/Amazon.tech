from django.contrib import admin
from .models import Program


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("name", "display_order")
    search_fields = ("name",)
    ordering = ("display_order",)