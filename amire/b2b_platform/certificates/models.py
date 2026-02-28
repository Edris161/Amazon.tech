from django.db import models
from companies.models import Company
import uuid


class Certificate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='certificates'
    )

    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='certificates/images/')
    pdf_file = models.FileField(upload_to='certificates/pdfs/', blank=True)

    def __str__(self):
        return self.name