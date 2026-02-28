from django.contrib import admin
from .models import Inquiry


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('company', 'sender_name', 'email', 'created_at')
    list_filter = ('company', 'created_at')
    search_fields = ('sender_name', 'email')