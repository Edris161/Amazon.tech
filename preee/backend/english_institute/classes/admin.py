"""
Classes admin configuration.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Class, Enrollment

class EnrollmentInline(admin.TabularInline):
    """
    Inline enrollment view for class admin.
    """
    model = Enrollment
    extra = 0
    fields = ('student', 'status', 'enrollment_date', 'notes')
    readonly_fields = ('enrollment_date',)
    autocomplete_fields = ['student']
    show_change_link = True

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    """
    Admin configuration for Class model.
    """
    list_display = (
        'name', 
        'level', 
        'teacher_name',
        'schedule',
        'enrollment_status',
        'capacity',
        'available_spots',
        'is_active',
        'start_date'
    )
    list_filter = ('level', 'is_active', 'start_date')
    search_fields = ('name', 'teacher_name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    # Add enrollment inline
    inlines = [EnrollmentInline]
    
    fieldsets = (
        ('Class Information', {
            'fields': (
                'name',
                'level',
                'teacher_name',
                'room',
                'capacity'
            )
        }),
        ('Schedule', {
            'fields': (
                'schedule',
                'start_date',
                'end_date'
            )
        }),
        ('Status', {
            'fields': (
                'is_active',
                'description'
            )
        }),
        ('System Information', {
            'fields': (
                'created_at',
                'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )
    
    def enrollment_status(self, obj):
        """Show enrollment status with color coding."""
        enrolled = obj.current_enrollment
        capacity = obj.capacity
        
        if obj.is_full:
            color = 'red'
            status = 'FULL'
        elif enrolled >= capacity * 0.8:
            color = 'orange'
            status = 'ALMOST FULL'
        else:
            color = 'green'
            status = 'AVAILABLE'
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">{} ({}/{})</span>',
            color, status, enrolled, capacity
        )
    enrollment_status.short_description = "Enrollment Status"
    
    def available_spots(self, obj):
        """Show available spots."""
        spots = obj.available_spots
        if spots <= 0:
            return format_html('<span style="color: red;">Full</span>')
        elif spots <= 5:
            return format_html('<span style="color: orange;">{} spots</span>', spots)
        return format_html('<span style="color: green;">{} spots</span>', spots)
    available_spots.short_description = "Available"

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    """
    Admin configuration for Enrollment model.
    """
    list_display = (
        'id',
        'student_info',
        'class_info',
        'status_colored',
        'enrollment_date'
    )
    list_filter = ('status', 'enrollment_date', 'class_enrolled__level')
    search_fields = (
        'student__first_name', 
        'student__last_name', 
        'student__student_id',
        'class_enrolled__name'
    )
    raw_id_fields = ('student', 'class_enrolled')
    readonly_fields = ('enrollment_date',)
    date_hierarchy = 'enrollment_date'
    
    def student_info(self, obj):
        """Show student details with link."""
        url = f"/admin/students/student/{obj.student.id}/change/"
        return format_html(
            '<a href="{}">{} - {}</a>',
            url,
            obj.student.student_id,
            obj.student
        )
    student_info.short_description = "Student"
    student_info.admin_order_field = 'student__last_name'
    
    def class_info(self, obj):
        """Show class details with link."""
        url = f"/admin/classes/class/{obj.class_enrolled.id}/change/"
        return format_html(
            '<a href="{}">{}</a>',
            url,
            obj.class_enrolled.name
        )
    class_info.short_description = "Class"
    class_info.admin_order_field = 'class_enrolled__name'
    
    def status_colored(self, obj):
        """Show status with color coding."""
        colors = {
            'enrolled': 'green',
            'completed': 'blue',
            'dropped': 'red',
            'waitlisted': 'orange'
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.status, 'black'),
            obj.get_status_display()
        )
    status_colored.short_description = "Status"