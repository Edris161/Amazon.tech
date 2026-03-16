# students/models.py
import uuid
from django.db import models

class Level(models.Model):
    name = models.CharField(max_length=50) # Beginner, Elementary, etc.

    def __str__(self):
        return self.name

class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    level = models.ForeignKey(Level, on_delete=models.PROTECT)
    registration_date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.student_id:
            # Generate ID like STU-2026-XXXX
            self.student_id = f"STU-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)
