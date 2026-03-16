# finance/views.py
from rest_framework import viewsets
from .models import Payment
from .serializers import PaymentSerializer
from users.permissions import IsFinanceUser

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsFinanceUser]  # Only Finance role can access
    filterset_fields = ['student', 'payment_type']

    def get_queryset(self):
        # Optional: Admins can see all, but maybe others only see specific data
        return super().get_queryset()
