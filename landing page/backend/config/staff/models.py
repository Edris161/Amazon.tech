from django.db import models

class Staff(models.Model):
    name = models.CharField(max_length=150)
    position = models.CharField(max_length=150)
    photo = models.ImageField(upload_to="staff/")
    bio = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name