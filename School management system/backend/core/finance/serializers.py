from rest_framework import serializers
from django.db.models import Sum
from students.serializers import StudentSerializer
from academics.serializers import ClassSerializer, AcademicYearSerializer
from .models import FeeStructure, FeeAssignment, Payment, Expense
from academics.models import AcademicYear, Class
from django.utils import timezone

class FeeStructureSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source='class_group.name', read_only=True, allow_null=True)
    academic_year_name = serializers.CharField(source='academic_year.name', read_only=True)
    
    class_id = serializers.PrimaryKeyRelatedField(
        queryset=Class.objects.all(),
        source='class_group',
        write_only=True,
        required=False,
        allow_null=True
    )
    academic_year_id = serializers.PrimaryKeyRelatedField(
        queryset=AcademicYear.objects.all(),
        source='academic_year',
        write_only=True
    )
    
    class Meta:
        model = FeeStructure
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
    
    def validate(self, data):
        if data.get('due_date') and data.get('due_date') < timezone.now().date():
            raise serializers.ValidationError("Due date cannot be in the past")
        return data

class FeeAssignmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.full_name', read_only=True)
    student_roll = serializers.CharField(source='student.roll_number', read_only=True)
    student_admission = serializers.CharField(source='student.admission_number', read_only=True)
    fee_name = serializers.CharField(source='fee_structure.name', read_only=True)
    fee_type = serializers.CharField(source='fee_structure.fee_type', read_only=True)
    class_name = serializers.CharField(source='fee_structure.class_group.name', read_only=True)
    paid_amount = serializers.SerializerMethodField()
    balance = serializers.SerializerMethodField()
    
    class Meta:
        model = FeeAssignment
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
    
    def get_paid_amount(self, obj):
        return obj.payments.filter(status='completed').aggregate(
            total=Sum('amount')
        )['total'] or 0
    
    def get_balance(self, obj):
        paid = self.get_paid_amount(obj)
        return obj.amount - paid
    
    def validate(self, data):
        # Check if assignment already exists
        if FeeAssignment.objects.filter(
            student=data['student'],
            fee_structure=data['fee_structure']
        ).exists() and not self.instance:
            raise serializers.ValidationError(
                "Fee already assigned to this student"
            )
        return data

class PaymentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.full_name', read_only=True)
    student_roll = serializers.CharField(source='student.roll_number', read_only=True)
    student_admission = serializers.CharField(source='student.admission_number', read_only=True)
    fee_name = serializers.CharField(source='fee_assignment.fee_structure.name', read_only=True, allow_null=True)
    received_by_name = serializers.CharField(source='received_by.full_name', read_only=True)
    receipt_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'receipt_number', 'received_by']
    
    def get_receipt_url(self, obj):
        if obj.receipt_pdf:
            return obj.receipt_pdf.url
        return None
    
    def create(self, validated_data):
        validated_data['received_by'] = self.context['request'].user
        payment = super().create(validated_data)
        
        # Update fee assignment status
        if payment.fee_assignment:
            total_paid = payment.fee_assignment.payments.filter(
                status='completed'
            ).aggregate(total=Sum('amount'))['total'] or 0
            
            if total_paid >= payment.fee_assignment.amount:
                payment.fee_assignment.status = 'paid'
            elif total_paid > 0:
                payment.fee_assignment.status = 'partial'
            payment.fee_assignment.save()
        
        return payment

class ExpenseSerializer(serializers.ModelSerializer):
    approved_by_name = serializers.CharField(source='approved_by.full_name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    invoice_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Expense
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'created_by', 'approved_by', 'approved_at']
    
    def get_invoice_url(self, obj):
        if obj.invoice_file:
            return obj.invoice_file.url
        return None
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

class FeePaymentSerializer(serializers.Serializer):
    fee_assignment_ids = serializers.ListField(child=serializers.IntegerField())
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    payment_method = serializers.ChoiceField(choices=Payment.PAYMENT_METHODS)
    transaction_id = serializers.CharField(required=False, allow_blank=True)
    remarks = serializers.CharField(required=False, allow_blank=True)

class FeeReportSerializer(serializers.Serializer):
    total_collected = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_pending = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_overdue = serializers.DecimalField(max_digits=15, decimal_places=2)
    collection_rate = serializers.FloatField()
    monthly_collection = serializers.ListField(child=serializers.DictField())
    fee_type_breakdown = serializers.ListField(child=serializers.DictField())
    class_wise_pending = serializers.ListField(child=serializers.DictField())