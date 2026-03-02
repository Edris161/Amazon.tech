from django.db import models
from students.models import Student
from teachers.models import Teacher

class Book(models.Model):
    CATEGORY_CHOICES = [
        ('textbook', 'Textbook'),
        ('reference', 'Reference'),
        ('fiction', 'Fiction'),
        ('non_fiction', 'Non-Fiction'),
        ('magazine', 'Magazine'),
        ('journal', 'Journal'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    isbn = models.CharField(max_length=20, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    edition = models.CharField(max_length=50, blank=True)
    publication_year = models.IntegerField()
    pages = models.IntegerField()
    language = models.CharField(max_length=50, default='English')
    location = models.CharField(max_length=100, blank=True)
    
    # Inventory
    total_copies = models.IntegerField(default=1)
    available_copies = models.IntegerField(default=1)
    rack_number = models.CharField(max_length=10, blank=True)
    
    # Additional info
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='library/covers/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['title']
        indexes = [
            models.Index(fields=['isbn']),
            models.Index(fields=['title']),
            models.Index(fields=['author']),
            models.Index(fields=['category']),
        ]
    
    def __str__(self):
        return f"{self.title} by {self.author}"

class BookIssue(models.Model):
    STATUS_CHOICES = [
        ('issued', 'Issued'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
        ('lost', 'Lost'),
        ('damaged', 'Damaged'),
    ]
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='issues')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    issued_to = models.CharField(max_length=10, choices=[('student', 'Student'), ('teacher', 'Teacher')])
    
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='issued')
    
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fine_paid = models.BooleanField(default=False)
    
    issued_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='+')
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-issue_date']
        indexes = [
            models.Index(fields=['book', 'status']),
            models.Index(fields=['due_date', 'status']),
        ]
    
    def __str__(self):
        borrower = self.student or self.teacher
        return f"{self.book.title} issued to {borrower}"
    
    @property
    def is_overdue(self):
        from django.utils import timezone
        return self.status == 'issued' and timezone.now().date() > self.due_date
    
    def calculate_fine(self):
        if self.is_overdue:
            days_overdue = (timezone.now().date() - self.due_date).days
            self.fine_amount = days_overdue * 10  # ₹10 per day
            self.save()

class BookReservation(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reservations')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    reserved_by = models.CharField(max_length=10, choices=[('student', 'Student'), ('teacher', 'Teacher')])
    reservation_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('available', 'Available'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ], default='pending')
    notified = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-reservation_date']
    
    def __str__(self):
        return f"{self.book.title} reserved"