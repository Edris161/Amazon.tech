from django.db import models


class Gallery(models.Model):
    title = models.CharField(
        max_length=150
    )

    image = models.ImageField(
        upload_to="gallery/",
        blank=True,
        null=True
    )

    category = models.CharField(
        max_length=100,
        db_index=True
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-uploaded_at"]
        verbose_name = "Gallery Image"
        verbose_name_plural = "Gallery"

    def __str__(self):
        return f"{self.title} ({self.category})"