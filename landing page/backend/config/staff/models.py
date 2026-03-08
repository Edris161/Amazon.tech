from django.db import models


class Staff(models.Model):
    name = models.CharField(max_length=150)
    position = models.CharField(max_length=150)

    photo = models.ImageField(
        upload_to="staff/",
        blank=True,
        null=True
    )

    bio = models.TextField(blank=True)

    email = models.EmailField(
        unique=True
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Staff Member"
        verbose_name_plural = "Staff Members"

    def __str__(self):
        return f"{self.name} - {self.position}"