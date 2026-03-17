"""
Finance admin configuration.
Registers Payment model with Django admin interface.
"""

from django.contrib import admin
from django.db.models import Sum
from django.utils.html import format_html
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """
    Admin configuration for Payment model.
    Provides comprehensive payment management interface.
    """
    
    # Display fields in list view
    list_display = (
        'reference_number', 
        'student_name', 
        'amount_display', 
        'payment_type', 
        'payment_date',
        'created_by_username',
        'created_at'
    )
    
    # Fields that link to detail view
    list_display_links = ('reference_number', 'student_name')
    
    # Filters in sidebar
    list_filter = (
        'payment_type', 
        'payment_date', 
        'created_at',
        'student__level'
    )
    
    # Search fields
    search_fields = (
        'reference_number', 
        'student__first_name', 
        'student__last_name', 
        'student__student_id',
        'note'
    )
    
    # Date hierarchy for easy navigation
    date_hierarchy = 'payment_date'
    
    # Default ordering
    ordering = ('-payment_date', '-created_at')
    
    # Fieldsets for detail view organization
    fieldsets = (
        ('Payment Information', {
            'fields': (
                'reference_number',
                'student',
                'amount',
                'payment_type',
                'payment_date'
            )
        }),
        ('Additional Information', {
            'fields': (
                'note',
                'created_by'
            ),
            'classes': ('collapse',)
        }),
    )
    
    # Read-only fields
    readonly_fields = ('reference_number', 'created_at', 'created_by')
    
    # Autocomplete fields
    autocomplete_fields = ['student', 'created_by']
    
    # List per page
    list_per_page = 25
    
    # Custom actions
    actions = ['mark_as_registration', 'mark_as_monthly', 'mark_as_books']
    
    def get_queryset(self, request):
        """
        Optimize queryset with select_related.
        """
        return super().get_queryset(request).select_related(
            'student', 
            'created_by'
        )
    
    def student_name(self, obj):
        """
        Return student full name with link to student admin.
        """
        if obj.student:
            url = f"/admin/students/student/{obj.student.id}/change/"
            return format_html('<a href="{}">{}</a>', url, obj.student)
        return "-"
    student_name.short_description = "Student"
    student_name.admin_order_field = 'student__last_name'
    
    def amount_display(self, obj):
        """
        Format amount with currency symbol.
        """
        return format_html('<b>${}</b>', obj.amount)
    amount_display.short_description = "Amount"
    amount_display.admin_order_field = 'amount'
    
    def created_by_username(self, obj):
        """
        Return username of creator.
        """
        return obj.created_by.username if obj.created_by else "-"
    created_by_username.short_description = "Created By"
    
    def save_model(self, request, obj, form, change):
        """
        Set created_by when saving new payment.
        """
        if not change:  # Only for new objects
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    # Custom actions
    def mark_as_registration(self, request, queryset):
        """
        Mark selected payments as registration fee.
        """
        updated = queryset.update(payment_type='registration')
        self.message_user(request, f'{updated} payments marked as registration fee.')
    mark_as_registration.short_description = "Mark as registration fee"
    
    def mark_as_monthly(self, request, queryset):
        """
        Mark selected payments as monthly fee.
        """
        updated = queryset.update(payment_type='monthly')
        self.message_user(request, f'{updated} payments marked as monthly fee.')
    mark_as_monthly.short_description = "Mark as monthly fee"
    
    def mark_as_books(self, request, queryset):
        """
        Mark selected payments as books fee.
        """
        updated = queryset.update(payment_type='books')
        self.message_user(request, f'{updated} payments marked as books fee.')
    mark_as_books.short_description = "Mark as books fee"

class PaymentInline(admin.TabularInline):
    """
    Inline payment view for student admin.
    """
    model = Payment
    extra = 0
    fields = ('reference_number', 'amount', 'payment_type', 'payment_date', 'created_by')
    readonly_fields = ('reference_number', 'created_by', 'payment_date')
    can_delete = True
    show_change_link = True
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('created_by')