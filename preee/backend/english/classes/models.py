# classes/models.py
from django.db import models
from students.models import Student, Level
from django.core.exceptions import ValidationError

class ClassRoom(models.Model):
    name = models.CharField(max_length=100)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    teacher_name = models.CharField(max_length=100)
    schedule = models.CharField(max_length=200) # e.g., Mon-Wed 5 PM
    capacity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, default='active')

    def clean(self):
        if self.classroom.enrollment_set.count() >= self.classroom.capacity:
            raise ValidationError("This class is already full.")
