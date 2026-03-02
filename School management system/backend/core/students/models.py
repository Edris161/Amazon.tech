from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User
from academics.models import Class, Section, AcademicYear

class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    admission_number = models.CharField(max_length=20, unique=True)
    roll_number = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True)
    
    # Academic info
    current_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)
    current_section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.SET_NULL, null=True)
    admission_date = models.DateField(auto_now_add=True)
    
    # Personal info
    place_of_birth = models.CharField(max_length=100, blank=True)
    nationality = models.CharField(max_length=50, default='Indian')
    religion = models.CharField(max_length=50, blank=True)
    caste = models.CharField(max_length=50, blank=True)
    mother_tongue = models.CharField(max_length=50, blank=True)
    
    # Address
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50, default='India')
    
    # Documents
    birth_certificate = models.FileField(upload_to='students/documents/', null=True, blank=True)
    previous_school = models.CharField(max_length=255, blank=True)
    previous_class = models.CharField(max_length=50, blank=True)
    medical_info = models.TextField(blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_alumni = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['admission_number']
        indexes = [
            models.Index(fields=['admission_number']),
            models.Index(fields=['roll_number']),
            models.Index(fields=['current_class', 'current_section']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.user.full_name} - {self.admission_number}"
    
    @property
    def name(self):
        return self.user.full_name

class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_profile')
    students = models.ManyToManyField(Student, related_name='parents')
    
    relationship = models.CharField(max_length=50)
    occupation = models.CharField(max_length=100, blank=True)
    qualification = models.CharField(max_length=100, blank=True)
    income = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    is_primary = models.BooleanField(default=False)
    can_receive_sms = models.BooleanField(default=True)
    can_receive_email = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.full_name} - Parent of {self.students.count()} students"

class StudentDocument(models.Model):
    DOCUMENT_TYPES = [
        ('birth', 'Birth Certificate'),
        ('address', 'Address Proof'),
        ('marksheet', 'Marksheet'),
        ('transfer', 'Transfer Certificate'),
        ('medical', 'Medical Record'),
        ('other', 'Other'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='students/documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-uploaded_at']

class StudentPromotion(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='promotions')
    from_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, related_name='+')
    from_section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, related_name='+')
    to_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, related_name='+')
    to_section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, related_name='+')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    promoted_on = models.DateField(auto_now_add=True)
    promoted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    remarks = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-promoted_on']