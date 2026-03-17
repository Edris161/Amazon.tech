from django.contrib import admin
from .models import Level, Student

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'order')
    list_editable = ('order',)
    search_fields = ('name', 'code')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'email', 'level', 'is_active')
    list_filter = ('level', 'is_active', 'registration_date')
    search_fields = ('student_id', 'first_name', 'last_name', 'email')
    readonly_fields = ('student_id', 'registration_date')
    
    