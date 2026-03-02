from django.db import models
from academics.models import Class, Subject, AcademicYear
from students.models import Student
from teachers.models import Teacher

class Exam(models.Model):
    EXAM_TYPES = [
        ('quarterly', 'Quarterly Exam'),
        ('half_yearly', 'Half Yearly Exam'),
        ('annual', 'Annual Exam'),
        ('unit_test', 'Unit Test'),
        ('pre_board', 'Pre-Board Exam'),
    ]
    
    name = models.CharField(max_length=255)
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPES)
    class_group = models.ForeignKey(Class, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)
    created_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['class_group', 'academic_year']),
            models.Index(fields=['is_published']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.class_group.name}"

class ExamSchedule(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='schedules')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_marks = models.IntegerField(default=100)
    pass_marks = models.IntegerField(default=35)
    room = models.CharField(max_length=50, blank=True)
    
    class Meta:
        ordering = ['date', 'start_time']
        unique_together = ['exam', 'subject']
    
    def __str__(self):
        return f"{self.exam.name} - {self.subject.name}"

class ExamResult(models.Model):
    exam_schedule = models.ForeignKey(ExamSchedule, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='exam_results')
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=2, blank=True)
    remarks = models.TextField(blank=True)
    entered_by = models.ForeignKey('teachers.Teacher', on_delete=models.SET_NULL, null=True)
    entered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['exam_schedule', 'student']
        ordering = ['student__roll_number']
    
    def __str__(self):
        return f"{self.student.user.full_name} - {self.marks_obtained}"
    
    def save(self, *args, **kwargs):
        # Calculate grade based on marks
        percentage = (self.marks_obtained / self.exam_schedule.max_marks) * 100
        if percentage >= 90:
            self.grade = 'A+'
        elif percentage >= 80:
            self.grade = 'A'
        elif percentage >= 70:
            self.grade = 'B+'
        elif percentage >= 60:
            self.grade = 'B'
        elif percentage >= 50:
            self.grade = 'C+'
        elif percentage >= 40:
            self.grade = 'C'
        elif percentage >= 33:
            self.grade = 'D'
        else:
            self.grade = 'F'
        super().save(*args, **kwargs)

class ReportCard(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='report_cards')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    total_marks = models.DecimalField(max_digits=6, decimal_places=2)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=2)
    rank = models.IntegerField(null=True, blank=True)
    result = models.CharField(max_length=20, choices=[
        ('pass', 'Pass'),
        ('fail', 'Fail'),
        ('distinction', 'Distinction'),
    ])
    pdf_file = models.FileField(upload_to='reports/', null=True, blank=True)
    generated_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'exam']
    
    def __str__(self):
        return f"{self.student.user.full_name} - {self.exam.name}"