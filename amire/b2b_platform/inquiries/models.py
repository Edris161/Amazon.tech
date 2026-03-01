from django.db import models
import uuid
from companies.models import Company
from products.models import Product


class Inquiry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='inquiries'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='inquiries'
    )

    buyer_name = models.CharField(max_length=255)
    buyer_email = models.EmailField()
    buyer_phone = models.CharField(max_length=50, blank=True)

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry for {self.product.name}"