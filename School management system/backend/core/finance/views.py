from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Sum, Count, Avg
from django.db.models.functions import TruncMonth, TruncDay
from django.utils import timezone
from datetime import timedelta, datetime
from .models import FeeStructure, FeeAssignment, Payment, Expense
from .serializers import (
    FeeStructureSerializer, FeeAssignmentSerializer,
    PaymentSerializer, ExpenseSerializer, FeePaymentSerializer,
    FeeReportSerializer
)
from students.models import Student
from accounts.models import AuditLog

class FeeStructureViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Fee Structure CRUD operations
    """
    queryset = FeeStructure.objects.all().select_related(
        'class_group', 'academic_year'
    ).order_by('-created_at')
    
    serializer_class = FeeStructureSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'class_group': ['exact', 'isnull'],
        'academic_year': ['exact'],
        'fee_type': ['exact'],
        'is_mandatory': ['exact'],
        'is_active': ['exact'],
        'due_date': ['gte', 'lte'],
    }
    search_fields = ['name', 'description']
    ordering_fields = ['amount', 'due_date', 'created_at']
    
    def perform_create(self, serializer):
        fee_structure = serializer.save()
        
        AuditLog.objects.create(
            user=self.request.user,
            action='CREATE',
            model_name='FeeStructure',
            object_id=str(fee_structure.id),
            changes=FeeStructureSerializer(fee_structure).data,
            ip_address=self.request.META.get('REMOTE_ADDR', '')
        )
    
    @action(detail=True, methods=['post'])
    def assign_to_students(self, request, pk=None):
        """Assign this fee structure to students"""
        fee_structure = self.get_object()
        
        class_id = request.data.get('class_id')
        section_id = request.data.get('section_id')
        student_ids = request.data.get('student_ids', [])
        
        if class_id:
            students = Student.objects.filter(
                current_class_id=class_id,
                is_active=True
            )
            if section_id:
                students = students.filter(current_section_id=section_id)
        elif student_ids:
            students = Student.objects.filter(id__in=student_ids)
        else:
            return Response(
                {'error': 'Either class_id or student_ids required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        assigned = []
        skipped = []
        
        for student in students:
            assignment, created = FeeAssignment.objects.get_or_create(
                student=student,
                fee_structure=fee_structure,
                defaults={
                    'amount': fee_structure.amount,
                    'due_date': fee_structure.due_date
                }
            )
            if created:
                assigned.append(student.id)
            else:
                skipped.append(student.id)
        
        AuditLog.objects.create(
            user=request.user,
            action='UPDATE',
            model_name='FeeStructure',
            object_id=str(fee_structure.id),
            changes={'assigned': len(assigned), 'skipped': len(skipped)},
            ip_address=request.META.get('REMOTE_ADDR', '')
        )
        
        return Response({
            'fee_structure': fee_structure.id,
            'assigned_count': len(assigned),
            'skipped_count': len(skipped),
            'assigned_students': assigned,
            'skipped_students': skipped
        })
    
    @action(detail=True, methods=['get'])
    def assignments(self, request, pk=None):
        """Get all assignments for this fee structure"""
        fee_structure = self.get_object()
        assignments = fee_structure.fee_assignments.all().select_related(
            'student__user'
        ).order_by('student__roll_number')
        
        serializer = FeeAssignmentSerializer(assignments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def collection_summary(self, request, pk=None):
        """Get collection summary for this fee structure"""
        fee_structure = self.get_object()
        
        assignments = fee_structure.fee_assignments.all()
        payments = Payment.objects.filter(fee_assignment__in=assignments)
        
        total_assigned = assignments.aggregate(total=Sum('amount'))['total'] or 0
        total_collected = payments.filter(status='completed').aggregate(
            total=Sum('amount')
        )['total'] or 0
        total_pending = total_assigned - total_collected
        
        paid_count = assignments.filter(status='paid').count()
        partial_count = assignments.filter(status='partial').count()
        pending_count = assignments.filter(status='pending').count()
        overdue_count = assignments.filter(status='overdue').count()
        
        return Response({
            'fee_structure': fee_structure.id,
            'name': fee_structure.name,
            'total_assigned': total_assigned,
            'total_collected': total_collected,
            'total_pending': total_pending,
            'collection_rate': round((total_collected / total_assigned * 100), 2) if total_assigned > 0 else 0,
            'paid_count': paid_count,
            'partial_count': partial_count,
            'pending_count': pending_count,
            'overdue_count': overdue_count
        })

class FeeAssignmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Fee Assignment CRUD operations
    """
    queryset = FeeAssignment.objects.all().select_related(
        'student__user', 'fee_structure'
    ).prefetch_related('payments').order_by('-due_date')
    
    serializer_class = FeeAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        'student': ['exact'],
        'fee_structure': ['exact'],
        'status': ['exact'],
        'due_date': ['gte', 'lte'],
        'created_at': ['gte', 'lte'],
    }
    search_fields = ['student__user__first_name', 'student__user__last_name', 'remarks']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by user role
        user = self.request.user
        if user.has_role('student'):
            student = user.student_profile
            if student:
                queryset = queryset.filter(student=student)
        elif user.has_role('parent'):
            parent = user.parent_profile
            if parent:
                queryset = queryset.filter(student__in=parent.students.all())
        
        return queryset
    
    def perform_create(self, serializer):
        assignment = serializer.save()
        
        AuditLog.objects.create(
            user=self.request.user,
            action='CREATE',
            model_name='FeeAssignment',
            object_id=str(assignment.id),
            changes=FeeAssignmentSerializer(assignment).data,
            ip_address=self.request.META.get('REMOTE_ADDR', '')
        )
    
    @action(detail=True, methods=['get'])
    def payments(self, request, pk=None):
        """Get all payments for this fee assignment"""
        assignment = self.get_object()
        payments = assignment.payments.all().order_by('-payment_date')
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def make_payment(self, request, pk=None):
        """Make a payment for this fee assignment"""
        assignment = self.get_object()
        
        amount = request.data.get('amount')
        payment_method = request.data.get('payment_method')
        transaction_id = request.data.get('transaction_id', '')
        remarks = request.data.get('remarks', '')
        
        if not amount or not payment_method:
            return Response(
                {'error': 'amount and payment_method required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Calculate balance
        paid_so_far = assignment.payments.filter(status='completed').aggregate(
            total=Sum('amount')
        )['total'] or 0
        balance = assignment.amount - paid_so_far
        
        if amount > balance:
            return Response(
                {'error': f'Amount exceeds balance of {balance}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        payment = Payment.objects.create(
            student=assignment.student,
            fee_assignment=assignment,
            amount=amount,
            payment_date=timezone.now().date(),
            payment_method=payment_method,
            transaction_id=transaction_id,
            remarks=remarks,
            status='completed',
            received_by=request.user
        )
        
        # Update assignment status
        new_paid = paid_so_far + amount
        if new_paid >= assignment.amount:
            assignment.status = 'paid'
        else:
            assignment.status = 'partial'
        assignment.save()
        
        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def waive(self, request, pk=None):
        """Waive this fee assignment"""
        assignment = self.get_object()
        
        if assignment.status == 'paid':
            return Response(
                {'error': 'Cannot waive a paid fee'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        assignment.status = 'waived'
        assignment.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='UPDATE',
            model_name='FeeAssignment',
            object_id=str(assignment.id),
            changes={'status': 'waived'},
            ip_address=request.META.get('REMOTE_ADDR', '')
        )
        
        return Response({'message': 'Fee waived successfully'})

class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Payment CRUD operations
    """
    queryset = Payment.objects.all().select_related(
        'student__user', 'fee_assignment__fee_structure', 'received_by'
    ).order_by('-payment_date')
    
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'student': ['exact'],
        'fee_assignment': ['exact'],
        'payment_method': ['exact'],
        'status': ['exact'],
        'payment_date': ['exact', 'gte', 'lte'],
        'received_by': ['exact'],
    }
    search_fields = ['receipt_number', 'transaction_id', 'remarks']
    ordering_fields = ['payment_date', 'amount', 'created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by user role
        user = self.request.user
        if user.has_role('student'):
            student = user.student_profile
            if student:
                queryset = queryset.filter(student=student)
        elif user.has_role('parent'):
            parent = user.parent_profile
            if parent:
                queryset = queryset.filter(student__in=parent.students.all())
        
        return queryset
    
    def perform_create(self, serializer):
        payment = serializer.save()
        
        AuditLog.objects.create(
            user=self.request.user,
            action='CREATE',
            model_name='Payment',
            object_id=str(payment.id),
            changes=PaymentSerializer(payment).data,
            ip_address=self.request.META.get('REMOTE_ADDR', '')
        )
    
    @action(detail=True, methods=['get'])
    def receipt(self, request, pk=None):
        """Generate and download payment receipt"""
        payment = self.get_object()
        
        # Generate receipt PDF if not exists
        if not payment.receipt_pdf:
            self.generate_receipt(payment)
        
        from django.http import FileResponse
        return FileResponse(
            payment.receipt_pdf.open(),
            as_attachment=True,
            filename=f"receipt_{payment.receipt_number}.pdf"
        )
    
    def generate_receipt(self, payment):
        """Generate PDF receipt"""
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        import io
        
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        
        # School header
        p.setFont("Helvetica-Bold", 20)
        p.drawString(200, 800, "School Name")
        p.setFont("Helvetica", 12)
        p.drawString(200, 780, "Address Line 1")
        p.drawString(200, 760, "City, State - PIN")
        p.drawString(200, 740, "Phone: 1234567890")
        
        # Receipt title
        p.setFont("Helvetica-Bold", 16)
        p.drawString(250, 700, f"PAYMENT RECEIPT")
        
        # Receipt details
        p.setFont("Helvetica", 12)
        p.drawString(50, 650, f"Receipt No: {payment.receipt_number}")
        p.drawString(50, 630, f"Date: {payment.payment_date}")
        p.drawString(50, 610, f"Student Name: {payment.student.user.full_name}")
        p.drawString(50, 590, f"Admission No: {payment.student.admission_number}")
        p.drawString(50, 570, f"Class: {payment.student.current_class.name} - {payment.student.current_section.name}")
        
        if payment.fee_assignment:
            p.drawString(50, 550, f"Fee Type: {payment.fee_assignment.fee_structure.name}")
        
        p.drawString(50, 530, f"Amount: ₹ {payment.amount}")
        p.drawString(50, 510, f"Payment Mode: {payment.get_payment_method_display()}")
        
        if payment.transaction_id:
            p.drawString(50, 490, f"Transaction ID: {payment.transaction_id}")
        
        # Footer
        p.drawString(50, 450, "Received by: " + (payment.received_by.full_name if payment.received_by else "System"))
        p.drawString(350, 450, "Authorized Signature")
        
        p.save()
        
        # Save PDF
        buffer.seek(0)
        filename = f"receipt_{payment.receipt_number}.pdf"
        payment.receipt_pdf.save(filename, buffer)
    
    @action(detail=False, methods=['get'])
    def daily_collection(self, request):
        """Get daily collection report"""
        date = request.query_params.get('date', timezone.now().date())
        
        payments = self.queryset.filter(
            payment_date=date,
            status='completed'
        )
        
        total = payments.aggregate(total=Sum('amount'))['total'] or 0
        count = payments.count()
        
        by_method = payments.values('payment_method').annotate(
            total=Sum('amount'),
            count=Count('id')
        )
        
        return Response({
            'date': date,
            'total_collection': total,
            'total_transactions': count,
            'by_method': by_method
        })
    
    @action(detail=False, methods=['get'])
    def monthly_report(self, request):
        """Get monthly collection report"""
        year = request.query_params.get('year', timezone.now().year)
        
        payments = self.queryset.filter(
            payment_date__year=year,
            status='completed'
        )
        
        monthly = payments.annotate(
            month=TruncMonth('payment_date')
        ).values('month').annotate(
            total=Sum('amount'),
            count=Count('id')
        ).order_by('month')
        
        return Response({
            'year': year,
            'monthly_data': monthly
        })

class ExpenseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Expense CRUD operations
    """
    queryset = Expense.objects.all().select_related(
        'approved_by', 'created_by'
    ).order_by('-expense_date')
    
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'category': ['exact'],
        'expense_date': ['exact', 'gte', 'lte'],
        'approved_by': ['exact'],
        'created_by': ['exact'],
    }
    search_fields = ['description', 'vendor', 'invoice_number']
    ordering_fields = ['expense_date', 'amount', 'created_at']
    
    def perform_create(self, serializer):
        expense = serializer.save()
        
        AuditLog.objects.create(
            user=self.request.user,
            action='CREATE',
            model_name='Expense',
            object_id=str(expense.id),
            changes=ExpenseSerializer(expense).data,
            ip_address=self.request.META.get('REMOTE_ADDR', '')
        )
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve expense"""
        expense = self.get_object()
        
        if expense.approved_by:
            return Response(
                {'error': 'Expense already approved'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        expense.approved_by = request.user
        expense.approved_at = timezone.now()
        expense.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='UPDATE',
            model_name='Expense',
            object_id=str(expense.id),
            changes={'approved': True, 'approved_by': request.user.id},
            ip_address=request.META.get('REMOTE_ADDR', '')
        )
        
        serializer = self.get_serializer(expense)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def category_summary(self, request):
        """Get expense summary by category"""
        year = request.query_params.get('year', timezone.now().year)
        
        expenses = self.queryset.filter(expense_date__year=year)
        
        by_category = expenses.values('category').annotate(
            total=Sum('amount'),
            count=Count('id')
        ).order_by('-total')
        
        monthly = expenses.annotate(
            month=TruncMonth('expense_date')
        ).values('month', 'category').annotate(
            total=Sum('amount')
        ).order_by('month')
        
        return Response({
            'year': year,
            'by_category': by_category,
            'monthly_breakdown': monthly
        })

class FinanceReportViewSet(viewsets.ViewSet):
    """
    ViewSet for financial reports
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Get finance dashboard summary"""
        # Current year
        current_year = timezone.now().year
        
        # Collections
        collections = Payment.objects.filter(
            status='completed',
            payment_date__year=current_year
        ).aggregate(
            total=Sum('amount'),
            count=Count('id')
        )
        
        # Monthly collection for chart
        monthly_collection = Payment.objects.filter(
            status='completed',
            payment_date__year=current_year
        ).annotate(
            month=TruncMonth('payment_date')
        ).values('month').annotate(
            total=Sum('amount')
        ).order_by('month')
        
        # Expenses
        expenses = Expense.objects.filter(
            expense_date__year=current_year
        ).aggregate(
            total=Sum('amount'),
            count=Count('id')
        )
        
        # Monthly expenses
        monthly_expense = Expense.objects.filter(
            expense_date__year=current_year
        ).annotate(
            month=TruncMonth('expense_date')
        ).values('month').annotate(
            total=Sum('amount')
        ).order_by('month')
        
        # Pending fees
        pending_fees = FeeAssignment.objects.filter(
            status__in=['pending', 'partial', 'overdue']
        ).aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        # Overdue fees
        overdue_fees = FeeAssignment.objects.filter(
            status='overdue',
            due_date__lt=timezone.now().date()
        ).aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        # Recent transactions
        recent_payments = Payment.objects.filter(
            status='completed'
        ).select_related(
            'student__user'
        ).order_by('-payment_date')[:10]
        
        recent_expenses = Expense.objects.order_by('-expense_date')[:5]
        
        return Response({
            'current_year': current_year,
            'collections': {
                'total': collections['total'] or 0,
                'count': collections['count'] or 0
            },
            'expenses': {
                'total': expenses['total'] or 0,
                'count': expenses['count'] or 0
            },
            'net_income': (collections['total'] or 0) - (expenses['total'] or 0),
            'pending_fees': pending_fees,
            'overdue_fees': overdue_fees,
            'monthly_collection': list(monthly_collection),
            'monthly_expense': list(monthly_expense),
            'recent_payments': PaymentSerializer(recent_payments, many=True).data,
            'recent_expenses': ExpenseSerializer(recent_expenses, many=True).data
        })
    
    @action(detail=False, methods=['get'])
    def fee_report(self, request):
        """Get comprehensive fee report"""
        class_id = request.query_params.get('class_id')
        section_id = request.query_params.get('section_id')
        
        assignments = FeeAssignment.objects.all()
        
        if class_id:
            assignments = assignments.filter(student__current_class_id=class_id)
        if section_id:
            assignments = assignments.filter(student__current_section_id=section_id)
        
        total_assigned = assignments.aggregate(total=Sum('amount'))['total'] or 0
        
        # Collections
        payments = Payment.objects.filter(
            fee_assignment__in=assignments,
            status='completed'
        )
        total_collected = payments.aggregate(total=Sum('amount'))['total'] or 0
        
        # By status
        by_status = assignments.values('status').annotate(
            count=Count('id'),
            total=Sum('amount')
        )
        
        # By class
        by_class = assignments.values(
            'student__current_class__name'
        ).annotate(
            total_assigned=Sum('amount'),
            total_collected=Sum('payments__amount', filter=Q(payments__status='completed')),
            count=Count('id')
        )
        
        # Overdue list
        overdue = assignments.filter(
            status='overdue',
            due_date__lt=timezone.now().date()
        ).select_related(
            'student__user', 'fee_structure'
        ).order_by('due_date')[:20]
        
        return Response({
            'summary': {
                'total_assigned': total_assigned,
                'total_collected': total_collected,
                'pending': total_assigned - total_collected,
                'collection_rate': round((total_collected / total_assigned * 100), 2) if total_assigned > 0 else 0
            },
            'by_status': by_status,
            'by_class': by_class,
            'overdue_list': FeeAssignmentSerializer(overdue, many=True).data
        })