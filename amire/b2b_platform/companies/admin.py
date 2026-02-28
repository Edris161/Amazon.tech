from django.contrib import admin
from .models import Company, CompanyTimeline


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('legal_name', 'business_type', 'is_verified', 'created_at')
    prepopulated_fields = {"slug": ("legal_name",)}
    search_fields = ('legal_name',)
    list_filter = ('business_type', 'is_verified')


@admin.register(CompanyTimeline)
class CompanyTimelineAdmin(admin.ModelAdmin):
    list_display = ('company', 'year')
    list_filter = ('year',)