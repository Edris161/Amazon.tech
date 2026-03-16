# finance/models.py
from django.db import models
from students.models import Student

class Payment(models.Model):
    PAYMENT_TYPES = (
        ('registration', 'Registration Fee'),
        ('monthly', 'Monthly Fee'),
        ('book', 'Book Fee'),
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    payment_date = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)
