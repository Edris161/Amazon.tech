from django.db import models
from students.models import Student
from teachers.models import Teacher
from academics.models import Class, Section, AcademicYear

class StudentAttendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('half_day', 'Half Day'),
        ('holiday', 'Holiday'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    class_group = models.ForeignKey(Class, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    remarks = models.TextField(blank=True)
    marked_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True)
    marked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'date']
        ordering = ['-date']
        indexes = [
            models.Index(fields=['student', 'date']),
            models.Index(fields=['class_group', 'section', 'date']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.student.user.full_name} - {self.date}"

class BulkAttendance(models.Model):
    class_group = models.ForeignKey(Class, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    date = models.DateField()
    attendance_data = models.JSONField()  # Store student_id: status mapping
    total_present = models.IntegerField(default=0)
    total_absent = models.IntegerField(default=0)
    total_students = models.IntegerField(default=0)
    marked_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True)
    marked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['class_group', 'section', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.class_group} {self.section} - {self.date}"

class Holiday(models.Model):
    HOLIDAY_TYPES = [
        ('national', 'National Holiday'),
        ('religious', 'Religious Holiday'),
        ('school', 'School Holiday'),
        ('event', 'Event'),
    ]
    
    name = models.CharField(max_length=255)
    date = models.DateField()
    holiday_type = models.CharField(max_length=20, choices=HOLIDAY_TYPES)
    description = models.TextField(blank=True)
    is_recurring = models.BooleanField(default=False)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['date']
        unique_together = ['name', 'date']
    
    def __str__(self):
        return f"{self.name} - {self.date}"