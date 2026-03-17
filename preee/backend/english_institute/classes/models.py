"""
Classes models module.
Defines Class and Enrollment models for the institute.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from students.models import Student, Level

class Class(models.Model):
    """
    Class model for English courses.
    Each class belongs to a level and has a teacher, schedule, and capacity.
    """
    
    name = models.CharField(max_length=100)
    level = models.ForeignKey(Level, on_delete=models.PROTECT, related_name='classes')
    teacher_name = models.CharField(max_length=100)
    schedule = models.CharField(max_length=200)  # e.g., "Mon/Wed 10:00-12:00"
    start_date = models.DateField()
    end_date = models.DateField()
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(50)])
    is_active = models.BooleanField(default=True)
    room = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "classes"
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['level', 'start_date']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.level.name}"
    
    @property
    def current_enrollment(self):
        """Return current number of enrolled students."""
        return self.enrollments.filter(status='enrolled').count()
    
    @property
    def available_spots(self):
        """Return number of available spots in the class."""
        return self.capacity - self.current_enrollment
    
    @property
    def is_full(self):
        """Check if class is full."""
        return self.current_enrollment >= self.capacity

class Enrollment(models.Model):
    """
    Enrollment model linking students to classes.
    Tracks enrollment status and date.
    """
    
    STATUS_CHOICES = (
        ('enrolled', 'Enrolled'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
        ('waitlisted', 'Waitlisted'),
    )
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    class_enrolled = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='enrolled')
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['student', 'class_enrolled']  # Prevent duplicate enrollments
        ordering = ['-enrollment_date']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['student', 'status']),
        ]
    
    def __str__(self):
        return f"{self.student} enrolled in {self.class_enrolled}"
    
    def save(self, *args, **kwargs):
        """
        Override save to prevent enrolling in full classes.
        """
        if not self.pk:  # Only check for new enrollments
            if self.class_enrolled.is_full and self.status == 'enrolled':
                self.status = 'waitlisted'
        
        super().save(*args, **kwargs)