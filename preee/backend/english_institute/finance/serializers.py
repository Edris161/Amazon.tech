"""
Finance serializers module.
Handles serialization of Payment data.
"""

from rest_framework import serializers
from .models import Payment
from students.serializers import StudentSerializer

class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for Payment model.
    Includes student details and created by user info.
    """
    
    student_name = serializers.CharField(source='student.__str__', read_only=True)
    student_details = StudentSerializer(source='student', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    payment_type_display = serializers.CharField(source='get_payment_type_display', read_only=True)
    
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('reference_number', 'created_at', 'created_by')
    
    def validate_amount(self, value):
        """
        Validate payment amount is positive.
        """
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        return value

class PaymentSummarySerializer(serializers.Serializer):
    """
    Serializer for payment summary statistics.
    """
    
    total_paid = serializers.DecimalField(max_digits=10, decimal_places=2)
    payment_type_breakdown = serializers.DictField()
    monthly_total = serializers.DecimalField(max_digits=10, decimal_places=2)