"""
Users models module.
Defines custom user model and roles for the institute.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Adds role-based access control for the institute.
    """
    
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('admission', 'Admission'),
        ('finance', 'Finance'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='admission')
    phone = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"