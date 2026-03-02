from django.db import models
from accounts.models import User
from academics.models import Subject

class Teacher(models.Model):
    EMPLOYMENT_TYPE = [
        ('permanent', 'Permanent'),
        ('contract', 'Contract'),
        ('probation', 'Probation'),
        ('intern', 'Intern'),
        ('visiting', 'Visiting'),
    ]
    
    QUALIFICATION_CHOICES = [
        ('bachelor', 'Bachelor\'s Degree'),
        ('master', 'Master\'s Degree'),
        ('phd', 'PhD'),
        ('diploma', 'Diploma'),
        ('certificate', 'Certificate'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    employee_id = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    
    # Employment details
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE)
    qualification = models.CharField(max_length=20, choices=QUALIFICATION_CHOICES)
    specialization = models.CharField(max_length=255)
    joining_date = models.DateField()
    leaving_date = models.DateField(null=True, blank=True)
    
    # Subjects taught
    subjects = models.ManyToManyField(Subject, related_name='teachers')
    
    # Contact
    emergency_contact_name = models.CharField(max_length=255)
    emergency_contact_phone = models.CharField(max_length=15)
    emergency_contact_relation = models.CharField(max_length=50)
    
    # Professional info
    experience_years = models.IntegerField(default=0)
    previous_school = models.CharField(max_length=255, blank=True)
    bank_account_no = models.CharField(max_length=50, blank=True)
    bank_name = models.CharField(max_length=100, blank=True)
    ifsc_code = models.CharField(max_length=20, blank=True)
    pan_number = models.CharField(max_length=10, blank=True)
    aadhar_number = models.CharField(max_length=12, blank=True)
    
    # Documents
    resume = models.FileField(upload_to='teachers/documents/', null=True, blank=True)
    qualification_docs = models.FileField(upload_to='teachers/documents/', null=True, blank=True)
    
    # Salary
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    allowances = models.JSONField(default=dict)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['employee_id']
        indexes = [
            models.Index(fields=['employee_id']),
            models.Index(fields=['joining_date']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.user.full_name} - {self.employee_id}"
    
    @property
    def total_salary(self):
        total = self.base_salary
        for allowance in self.allowances.values():
            total += allowance
        return total

class TeacherAttendance(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('half_day', 'Half Day'),
        ('leave', 'On Leave'),
    ])
    remarks = models.TextField(blank=True)
    marked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        unique_together = ['teacher', 'date']
        ordering = ['-date']
        indexes = [
            models.Index(fields=['teacher', 'date']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.teacher.user.full_name} - {self.date}"

class TeacherLeave(models.Model):
    LEAVE_TYPES = [
        ('sick', 'Sick Leave'),
        ('casual', 'Casual Leave'),
        ('earned', 'Earned Leave'),
        ('maternity', 'Maternity Leave'),
        ('paternity', 'Paternity Leave'),
        ('unpaid', 'Unpaid Leave'),
    ]
    
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='leaves')
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ], default='pending')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='+')
    approved_on = models.DateTimeField(null=True, blank=True)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.teacher.user.full_name} - {self.leave_type}"
    
    @property
    def days_count(self):
        return (self.to_date - self.from_date).days + 1