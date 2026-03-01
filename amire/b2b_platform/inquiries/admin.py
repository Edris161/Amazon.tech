from django.contrib import admin
from .models import Inquiry


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'company',
        'buyer_name',
        'buyer_email',
        'created_at',
    )

    search_fields = (
        'buyer_name',
        'buyer_email',
        'product__name',
        'company__legal_name',
    )

    list_filter = (
        'created_at',
    )