from django.db import models
from students.models import Student
from academics.models import Class, AcademicYear

class FeeStructure(models.Model):
    FEE_TYPES = [
        ('tuition', 'Tuition Fee'),
        ('admission', 'Admission Fee'),
        ('exam', 'Exam Fee'),
        ('sports', 'Sports Fee'),
        ('library', 'Library Fee'),
        ('transport', 'Transport Fee'),
        ('hostel', 'Hostel Fee'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=255)
    fee_type = models.CharField(max_length=20, choices=FEE_TYPES)
    class_group = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, blank=True)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_mandatory = models.BooleanField(default=True)
    due_date = models.DateField()
    late_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.amount}"

class FeeAssignment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fee_assignments')
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('partial', 'Partially Paid'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('waived', 'Waived'),
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'fee_structure']
        indexes = [
            models.Index(fields=['student', 'status']),
            models.Index(fields=['due_date', 'status']),
        ]
    
    def __str__(self):
        return f"{self.student.user.full_name} - {self.fee_structure.name}"

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('card', 'Credit/Debit Card'),
        ('bank', 'Bank Transfer'),
        ('cheque', 'Cheque'),
        ('online', 'Online Payment'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    fee_assignment = models.ForeignKey(FeeAssignment, on_delete=models.CASCADE, null=True)
    receipt_number = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    transaction_id = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    remarks = models.TextField(blank=True)
    received_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True)
    receipt_pdf = models.FileField(upload_to='receipts/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-payment_date']
        indexes = [
            models.Index(fields=['receipt_number']),
            models.Index(fields=['student', 'payment_date']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Receipt {self.receipt_number} - {self.amount}"
    
    def save(self, *args, **kwargs):
        if not self.receipt_number:
            # Generate receipt number
            last_payment = Payment.objects.order_by('-id').first()
            next_id = (last_payment.id + 1) if last_payment else 1
            self.receipt_number = f"RCP-{self.payment_date.strftime('%Y%m')}-{next_id:06d}"
        super().save(*args, **kwargs)

class Expense(models.Model):
    EXPENSE_CATEGORIES = [
        ('salary', 'Salary'),
        ('maintenance', 'Maintenance'),
        ('utilities', 'Utilities'),
        ('supplies', 'Supplies'),
        ('equipment', 'Equipment'),
        ('events', 'Events'),
        ('other', 'Other'),
    ]
    
    category = models.CharField(max_length=20, choices=EXPENSE_CATEGORIES)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense_date = models.DateField()
    vendor = models.CharField(max_length=255, blank=True)
    invoice_number = models.CharField(max_length=50, blank=True)
    invoice_file = models.FileField(upload_to='expenses/', null=True, blank=True)
    approved_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='+')
    approved_at = models.DateTimeField(null=True, blank=True)
    remarks = models.TextField(blank=True)
    created_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-expense_date']
    
    def __str__(self):
        return f"{self.category} - {self.amount}"