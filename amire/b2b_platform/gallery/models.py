from django.db import models
from companies.models import Company
import uuid


class Media(models.Model):
    MEDIA_TYPES = [
        ('factory', 'Factory Overview'),
        ('production', 'Production Line'),
        ('showroom', 'Showroom'),
        ('video', 'Intro Video'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='media'
    )

    media_type = models.CharField(max_length=50, choices=MEDIA_TYPES)
    file = models.FileField(upload_to='company_media/')

    def __str__(self):
        return f"{self.company.legal_name} - {self.media_type}"