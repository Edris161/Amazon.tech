from rest_framework import generics
from django.core.mail import send_mail
from django.conf import settings
from .models import Inquiry
from .serializers import InquirySerializer


class InquiryCreateView(generics.CreateAPIView):
    queryset = Inquiry.objects.all()
    serializer_class = InquirySerializer

    def perform_create(self, serializer):
        inquiry = serializer.save()

        subject = f"New Inquiry for {inquiry.product.name}"

        message = f"""
        You received a new inquiry.

        Product: {inquiry.product.name}
        Company: {inquiry.company.legal_name}

        Buyer Name: {inquiry.buyer_name}
        Buyer Email: {inquiry.buyer_email}
        Buyer Phone: {inquiry.buyer_phone}

        Message:
        {inquiry.message}
        """

        # Send email to company
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [inquiry.company.email],
            fail_silently=False,
        )

        # Send email to admin
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )