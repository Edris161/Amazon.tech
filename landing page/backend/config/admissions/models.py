from django.db import models

class Admission(models.Model):
    student_name = models.CharField(max_length=150)
    father_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    grade = models.CharField(max_length=50)
    message = models.TextField()
    status = models.CharField(max_length=20, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student_name