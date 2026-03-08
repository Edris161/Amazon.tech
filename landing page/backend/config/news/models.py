from django.db import models
from django.utils.text import slugify


class News(models.Model):
    title = models.CharField(max_length=200)

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    short_description = models.TextField()

    content = models.TextField()

    image = models.ImageField(
        upload_to="news/",
        blank=True,
        null=True
    )

    published_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-published_at"]
        verbose_name = "News"
        verbose_name_plural = "News"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            num = 1

            while News.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title