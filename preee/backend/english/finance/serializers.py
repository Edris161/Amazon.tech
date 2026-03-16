# finance/serializers.py
from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    student_name = serializers.ReadOnlyField(source='student.first_name')

    class Meta:
        model = Payment
        fields = ['id', 'student', 'student_name', 'amount', 
                  'payment_type', 'payment_date', 'note']
