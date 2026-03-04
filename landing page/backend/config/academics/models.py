from django.db import models

class Academics(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    grade_level = models.CharField(max_length=100)
    subjects = models.TextField()
    duration = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title