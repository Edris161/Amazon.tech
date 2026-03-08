from django.db import models


class Academics(models.Model):
    title = models.CharField(
        max_length=200
    )

    description = models.TextField()

    grade_level = models.CharField(
        max_length=100
    )

    subjects = models.TextField(
        blank=True
    )

    duration = models.CharField(
        max_length=100
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Academic Program"
        verbose_name_plural = "Academics"

    def __str__(self):
        return f"{self.title} - {self.grade_level}"