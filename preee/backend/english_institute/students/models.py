"""
Students models module.
Defines Student and Level models for the institute.
"""

from django.db import models
from django.core.validators import MinLengthValidator
import uuid

class Level(models.Model):
    """
    English proficiency levels.
    Examples: Beginner, Elementary, Intermediate, Advanced
    """
    
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)  # For ordering levels
    
    class Meta:
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name

class Student(models.Model):
    """
    Student model for the English institute.
    Each student gets a unique ID and belongs to one level.
    """
    
    # Generate unique student ID (e.g., STU2024001)
    student_id = models.CharField(max_length=20, unique=True, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, validators=[MinLengthValidator(10)])
    level = models.ForeignKey(Level, on_delete=models.PROTECT, related_name='students')
    registration_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-registration_date']
        indexes = [
            models.Index(fields=['student_id']),
            models.Index(fields=['email']),
            models.Index(fields=['is_active']),
        ]
    
    def save(self, *args, **kwargs):
        """
        Override save to generate student_id if not exists.
        """
        if not self.student_id:
            # Generate student ID: STU + year + sequential number
            year = self.registration_date.strftime('%Y') if self.registration_date else '2024'
            last_student = Student.objects.filter(
                student_id__startswith=f'STU{year}'
            ).order_by('student_id').last()
            
            if last_student:
                last_number = int(last_student.student_id[-3:])
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.student_id = f'STU{year}{new_number:03d}'
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.student_id} - {self.first_name} {self.last_name}"