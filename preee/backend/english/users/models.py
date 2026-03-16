# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLES = (
        ('admin', 'Admin'),
        ('admission', 'Admission'),
        ('finance', 'Finance'),
    )
    role = models.CharField(max_length=20, choices=ROLES, default='admission')
