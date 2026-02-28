import uuid
from django.db import models
from django.utils.text import slugify


class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True, blank=True)

    LEGAL_TYPES = [
        ('manufacturer', 'Manufacturer'),
        ('trading', 'Trading Company'),
        ('wholesaler', 'Wholesaler'),
    ]

    legal_name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    business_type = models.CharField(max_length=50, choices=LEGAL_TYPES)
    is_verified = models.BooleanField(default=False)
    established_year = models.PositiveIntegerField()

    description = models.TextField()

    factory_size = models.CharField(max_length=100, blank=True)
    total_employees = models.PositiveIntegerField(null=True, blank=True)
    annual_output_value = models.CharField(max_length=100, blank=True)

    main_markets = models.CharField(max_length=255, blank=True)

    address = models.TextField()
    contact_person = models.CharField(max_length=150)
    phone = models.CharField(max_length=50)
    email = models.EmailField()

    website = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    whatsapp = models.CharField(max_length=50, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.legal_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.legal_name


# ✅ IMPORTANT: This must be OUTSIDE Company class
class CompanyTimeline(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='timeline'
    )
    year = models.PositiveIntegerField()
    event = models.TextField()

    class Meta:
        ordering = ['-year']

    def __str__(self):
        return f"{self.company.legal_name} - {self.year}"