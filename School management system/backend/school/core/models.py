from django.db import models


class SiteSetting(models.Model):
    school_name = models.CharField(max_length=255)
    tagline = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='site/')
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    twitter = models.URLField(blank=True)

    def __str__(self):
        return self.school_name