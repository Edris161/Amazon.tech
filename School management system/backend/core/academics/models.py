from django.db import models

class AcademicYear(models.Model):
    name = models.CharField(max_length=50, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.is_active:
            # Deactivate all other academic years
            AcademicYear.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)

class Class(models.Model):
    name = models.CharField(max_length=50)  # e.g., "Class 1", "Grade 1"
    code = models.CharField(max_length=10, unique=True)
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Classes"
        ordering = ['display_order']
    
    def __str__(self):
        return self.name

class Section(models.Model):
    class_group = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='sections')
    name = models.CharField(max_length=10)  # e.g., "A", "B", "C"
    capacity = models.IntegerField(default=30)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['class_group', 'name']
        ordering = ['class_group__display_order', 'name']
    
    def __str__(self):
        return f"{self.class_group.name} - Section {self.name}"

class Subject(models.Model):
    SUBJECT_TYPES = [
        ('core', 'Core'),
        ('elective', 'Elective'),
        ('language', 'Language'),
        ('co_curricular', 'Co-curricular'),
    ]
    
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    subject_type = models.CharField(max_length=20, choices=SUBJECT_TYPES)
    classes = models.ManyToManyField(Class, related_name='subjects')
    max_marks = models.IntegerField(default=100)
    pass_marks = models.IntegerField(default=35)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Timetable(models.Model):
    DAYS_OF_WEEK = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
    ]
    
    class_group = models.ForeignKey(Class, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey('teachers.Teacher', on_delete=models.CASCADE)
    day = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=50, blank=True)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['day', 'start_time']
        indexes = [
            models.Index(fields=['class_group', 'section', 'day']),
            models.Index(fields=['teacher', 'day']),
        ]
    
    def __str__(self):
        return f"{self.class_group} {self.section} - {self.subject} ({self.day})"