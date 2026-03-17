"""
Finance views module.
Handles API endpoints for payment management and reporting.
"""

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import Payment
from .serializers import PaymentSerializer, PaymentSummarySerializer

class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Payment model.
    
    Provides comprehensive payment management endpoints.
    
    Endpoints:
    - GET /payments/ - List all payments
    - POST /payments/ - Record new payment
    - GET /payments/{id}/ - Retrieve payment details
    - PUT /payments/{id}/ - Update payment
    - DELETE /payments/{id}/ - Delete payment
    - GET /payments/student/{student_id}/ - Get student payment history
    - GET /payments/summary/ - Get payment summary statistics
    - GET /payments/recent/ - Get recent payments
    """
    
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['student', 'payment_type', 'payment_date']
    search_fields = ['student__first_name', 'student__last_name', 'reference_number', 'note']
    ordering_fields = ['payment_date', 'amount', 'created_at']
    ordering = ['-payment_date', '-created_at']
    
    def perform_create(self, serializer):
        """
        Set created_by to current user when creating payment.
        """
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'], url_path='student/(?P<student_id>[^/.]+)')
    def student_payments(self, request, student_id=None):
        """
        Get payment history for a specific student.
        """
        payments = self.queryset.filter(student_id=student_id)
        
        # Calculate total paid
        total = payments.aggregate(total=Sum('amount'))['total'] or 0
        
        page = self.paginate_queryset(payments)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'payments': serializer.data,
                'total_paid': total,
                'payment_count': payments.count()
            })
        
        serializer = self.get_serializer(payments, many=True)
        return Response({
            'payments': serializer.data,
            'total_paid': total,
            'payment_count': payments.count()
        })
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        Get payment summary statistics.
        """
        # Date filters
        today = timezone.now().date()
        thirty_days_ago = today - timedelta(days=30)
        
        # All payments
        all_payments = self.queryset
        
        # Summary statistics
        total_paid = all_payments.aggregate(total=Sum('amount'))['total'] or 0
        
        # Breakdown by payment type
        type_breakdown = all_payments.values('payment_type').annotate(
            total=Sum('amount'),
            count=Count('id')
        ).order_by('payment_type')
        
        type_dict = {}
        for item in type_breakdown:
            type_dict[item['payment_type']] = {
                'total': item['total'],
                'count': item['count']
            }
        
        # Monthly total (last 30 days)
        monthly_payments = all_payments.filter(payment_date__gte=thirty_days_ago)
        monthly_total = monthly_payments.aggregate(total=Sum('amount'))['total'] or 0
        
        # Recent payments (last 7 days)
        recent_payments = all_payments.filter(payment_date__gte=today - timedelta(days=7))
        recent_serializer = self.get_serializer(recent_payments[:10], many=True)
        
        return Response({
            'summary': {
                'total_paid': total_paid,
                'total_transactions': all_payments.count(),
                'monthly_total': monthly_total,
                'monthly_transactions': monthly_payments.count(),
                'payment_type_breakdown': type_dict
            },
            'recent_payments': recent_serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """
        Get recent payments (last 7 days).
        """
        today = timezone.now().date()
        seven_days_ago = today - timedelta(days=7)
        
        recent_payments = self.queryset.filter(payment_date__gte=seven_days_ago)
        
        page = self.paginate_queryset(recent_payments)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(recent_payments, many=True)
        return Response(serializer.data)