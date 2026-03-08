from django.db import models


class Admission(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    student_name = models.CharField(
        max_length=150
    )

    father_name = models.CharField(
        max_length=150
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    grade = models.CharField(
        max_length=50
    )

    message = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Admission Application"
        verbose_name_plural = "Admissions"

    def __str__(self):
        return f"{self.student_name} - {self.grade}"