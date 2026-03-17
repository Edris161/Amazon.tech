"""
Finance models module.
Defines Payment model for tracking student payments.
"""

from django.db import models
from django.core.validators import MinValueValidator
from students.models import Student

class Payment(models.Model):
    """
    Payment model for tracking student financial transactions.
    Supports different payment types and includes notes.
    """
    
    PAYMENT_TYPES = (
        ('registration', 'Registration Fee'),
        ('monthly', 'Monthly Fee'),
        ('books', 'Books Fee'),
        ('other', 'Other'),
    )
    
    student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    payment_date = models.DateField(auto_now_add=True)
    reference_number = models.CharField(max_length=50, unique=True, blank=True)
    note = models.TextField(blank=True)
    created_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-payment_date', '-created_at']
        indexes = [
            models.Index(fields=['student', 'payment_date']),
            models.Index(fields=['payment_type']),
            models.Index(fields=['reference_number']),
        ]
    
    def save(self, *args, **kwargs):
        """
        Override save to generate reference number if not exists.
        """
        if not self.reference_number:
            # Generate reference number: PAY + year + month + random number
            import random
            from datetime import datetime
            
            year_month = datetime.now().strftime('%Y%m')
            random_num = random.randint(1000, 9999)
            self.reference_number = f"PAY{year_month}{random_num}"
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.reference_number} - {self.student} - {self.amount}"