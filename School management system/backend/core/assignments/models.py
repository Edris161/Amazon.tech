from django.db import models
from academics.models import Class, Section, Subject
from teachers.models import Teacher
from students.models import Student

class Assignment(models.Model):
    ASSIGNMENT_TYPES = [
        ('homework', 'Homework'),
        ('classwork', 'Classwork'),
        ('project', 'Project'),
        ('assignment', 'Assignment'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    assignment_type = models.CharField(max_length=20, choices=ASSIGNMENT_TYPES)
    class_group = models.ForeignKey(Class, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    due_date = models.DateTimeField()
    max_marks = models.IntegerField(default=100)
    attachment = models.FileField(upload_to='assignments/', null=True, blank=True)
    instructions = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-due_date']
        indexes = [
            models.Index(fields=['class_group', 'section', 'subject']),
            models.Index(fields=['due_date']),
            models.Index(fields=['teacher']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.class_group} {self.section}"

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='submissions')
    submission_date = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(upload_to='submissions/', null=True, blank=True)
    comments = models.TextField(blank=True)
    
    # Grading
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True)
    graded_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    graded_at = models.DateTimeField(null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=[
        ('submitted', 'Submitted'),
        ('late', 'Late Submission'),
        ('graded', 'Graded'),
        ('returned', 'Returned'),
    ], default='submitted')
    
    class Meta:
        unique_together = ['assignment', 'student']
        ordering = ['-submission_date']
    
    def __str__(self):
        return f"{self.student.user.full_name} - {self.assignment.title}"
    
    @property
    def is_late(self):
        return self.submission_date > self.assignment.due_date
    
    def save(self, *args, **kwargs):
        if self.is_late and self.status == 'submitted':
            self.status = 'late'
        super().save(*args, **kwargs)