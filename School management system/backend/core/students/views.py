from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from django.utils import timezone
import csv
import io
import pandas as pd
from .models import Student, Parent, StudentDocument, StudentPromotion
from .serializers import (
    StudentSerializer, ParentSerializer, StudentDocumentSerializer,
    StudentPromotionSerializer, StudentBulkUploadSerializer, StudentSearchSerializer
)
from accounts.models import User, AuditLog
from academics.models import Class, Section, AcademicYear

class StudentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Student CRUD operations with filtering, searching and bulk operations
    """
    queryset = Student.objects.all().select_related(
        'user', 'current_class', 'current_section', 'academic_year'
    ).prefetch_related('parents', 'documents', 'promotions').order_by('-admission_date')
    
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'current_class': ['exact'],
        'current_section': ['exact'],
        'academic_year': ['exact'],
        'is_active': ['exact'],
        'is_alumni': ['exact'],
        'gender': ['exact'],
        'blood_group': ['exact'],
        'admission_date': ['gte', 'lte', 'exact'],
        'date_of_birth': ['gte', 'lte', 'exact'],
    }
    search_fields = [
        'user__first_name', 'user__last_name', 'user__email',
        'admission_number', 'roll_number', 'user__phone'
    ]
    ordering_fields = [
        'admission_number', 'user__first_name', 'user__last_name',
        'admission_date', 'current_class__name'
    ]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by user role
        user = self.request.user
        if user.has_role('teacher'):
            # Teachers see students in their classes
            teacher = user.teacher_profile
            if teacher:
                queryset = queryset.filter(
                    current_class__in=teacher.classes.all()
                )
        elif user.has_role('parent'):
            # Parents see their own children
            parent = user.parent_profile
            if parent:
                queryset = queryset.filter(parents=parent)
        elif user.has_role('student'):
            # Students see only themselves
            student = user.student_profile
            if student:
                queryset = queryset.filter(id=student.id)
        
        return queryset
    
    def perform_create(self, serializer):
        student = serializer.save()
        
        # Create audit log
        AuditLog.objects.create(
            user=self.request.user,
            action='CREATE',
            model_name='Student',
            object_id=str(student.id),
            changes=StudentSerializer(student).data,
            ip_address=self.request.META.get('REMOTE_ADDR', '')
        )
    
    def perform_update(self, serializer):
        old_data = StudentSerializer(self.get_object()).data
        student = serializer.save()
        
        AuditLog.objects.create(
            user=self.request.user,
            action='UPDATE',
            model_name='Student',
            object_id=str(student.id),
            changes={'old': old_data, 'new': StudentSerializer(student).data},
            ip_address=self.request.META.get('REMOTE_ADDR', '')
        )
    
    def perform_destroy(self, instance):
        AuditLog.objects.create(
            user=self.request.user,
            action='DELETE',
            model_name='Student',
            object_id=str(instance.id),
            changes={'admission_number': instance.admission_number},
            ip_address=self.request.META.get('REMOTE_ADDR', '')
        )
        instance.delete()
    
    @action(detail=True, methods=['get'])
    def parents(self, request, pk=None):
        """Get all parents of a student"""
        student = self.get_object()
        parents = student.parents.all()
        serializer = ParentSerializer(parents, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def documents(self, request, pk=None):
        """Get all documents of a student"""
        student = self.get_object()
        documents = student.documents.all().order_by('-uploaded_at')
        serializer = StudentDocumentSerializer(documents, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def promotions(self, request, pk=None):
        """Get promotion history of a student"""
        student = self.get_object()
        promotions = student.promotions.all().order_by('-promoted_on')
        serializer = StudentPromotionSerializer(promotions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def attendance(self, request, pk=None):
        """Get attendance records for a student"""
        student = self.get_object()
        from attendance.models import StudentAttendance
        from attendance.serializers import StudentAttendanceSerializer
        
        # Get date filters from query params
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        attendances = StudentAttendance.objects.filter(student=student)
        
        if start_date:
            attendances = attendances.filter(date__gte=start_date)
        if end_date:
            attendances = attendances.filter(date__lte=end_date)
        
        attendances = attendances.order_by('-date')[:100]
        serializer = StudentAttendanceSerializer(attendances, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        """Get exam results for a student"""
        student = self.get_object()
        from exams.models import ExamResult
        from exams.serializers import ExamResultSerializer
        
        results = ExamResult.objects.filter(
            student=student
        ).select_related(
            'exam_schedule__exam',
            'exam_schedule__subject'
        ).order_by('-exam_schedule__exam__start_date')
        
        serializer = ExamResultSerializer(results, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def fees(self, request, pk=None):
        """Get fee assignments and payments for a student"""
        student = self.get_object()
        from finance.models import FeeAssignment, Payment
        from finance.serializers import FeeAssignmentSerializer, PaymentSerializer
        
        fee_assignments = FeeAssignment.objects.filter(student=student)
        payments = Payment.objects.filter(student=student).order_by('-payment_date')[:20]
        
        return Response({
            'fee_assignments': FeeAssignmentSerializer(fee_assignments, many=True).data,
            'recent_payments': PaymentSerializer(payments, many=True).data
        })
    
    @action(detail=True, methods=['post'])
    def promote(self, request, pk=None):
        """Promote student to next class"""
        student = self.get_object()
        
        to_class_id = request.data.get('to_class')
        to_section_id = request.data.get('to_section')
        academic_year_id = request.data.get('academic_year')
        remarks = request.data.get('remarks', '')
        
        # Validate required fields
        if not all([to_class_id, to_section_id, academic_year_id]):
            return Response(
                {'error': 'to_class, to_section, and academic_year are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if class and section exist
        try:
            to_class = Class.objects.get(id=to_class_id)
            to_section = Section.objects.get(id=to_section_id)
            academic_year = AcademicYear.objects.get(id=academic_year_id)
        except (Class.DoesNotExist, Section.DoesNotExist, AcademicYear.DoesNotExist):
            return Response(
                {'error': 'Invalid class, section, or academic year'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create promotion record
        promotion = StudentPromotion.objects.create(
            student=student,
            from_class=student.current_class,
            from_section=student.current_section,
            to_class=to_class,
            to_section=to_section,
            academic_year=academic_year,
            promoted_by=request.user,
            remarks=remarks
        )
        
        # Update student's current class and section
        student.current_class = to_class
        student.current_section = to_section
        student.academic_year = academic_year
        student.save()
        
        # Create audit log
        AuditLog.objects.create(
            user=request.user,
            action='UPDATE',
            model_name='Student',
            object_id=str(student.id),
            changes={'promotion': StudentPromotionSerializer(promotion).data},
            ip_address=request.META.get('REMOTE_ADDR', '')
        )
        
        serializer = StudentPromotionSerializer(promotion)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """Toggle student active status"""
        student = self.get_object()
        student.is_active = not student.is_active
        student.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='UPDATE',
            model_name='Student',
            object_id=str(student.id),
            changes={'is_active': student.is_active},
            ip_address=request.META.get('REMOTE_ADDR', '')
        )
        
        return Response({'is_active': student.is_active})
    
    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """Bulk create students from CSV/Excel"""
        serializer = StudentBulkUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        file = serializer.validated_data['file']
        
        # Read file
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        
        created_students = []
        errors = []
        
        for index, row in df.iterrows():
            try:
                # Create user first
                user = User.objects.create_user(
                    email=row.get('email'),
                    first_name=row.get('first_name'),
                    last_name=row.get('last_name'),
                    password='DefaultPass123'  # Default password, should be changed
                )
                
                # Get or create student
                student = Student.objects.create(
                    user=user,
                    admission_number=row.get('admission_number'),
                    roll_number=row.get('roll_number'),
                    date_of_birth=row.get('date_of_birth'),
                    gender=row.get('gender'),
                    blood_group=row.get('blood_group', ''),
                    address_line1=row.get('address_line1'),
                    city=row.get('city'),
                    state=row.get('state'),
                    postal_code=row.get('postal_code'),
                    country=row.get('country', 'India')
                )
                
                created_students.append(StudentSerializer(student).data)
                
            except Exception as e:
                errors.append({'row': index + 2, 'error': str(e)})
        
        AuditLog.objects.create(
            user=request.user,
            action='CREATE',
            model_name='Student',
            object_id='bulk',
            changes={'count': len(created_students), 'errors': errors},
            ip_address=request.META.get('REMOTE_ADDR', '')
        )
        
        return Response({
            'created': len(created_students),
            'students': created_students,
            'errors': errors
        })
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get student statistics"""
        total = Student.objects.count()
        active = Student.objects.filter(is_active=True).count()
        alumni = Student.objects.filter(is_alumni=True).count()
        
        class_distribution = Student.objects.filter(
            is_active=True
        ).values(
            'current_class__name'
        ).annotate(
            count=Count('id')
        ).order_by('current_class__name')
        
        gender_distribution = Student.objects.filter(
            is_active=True
        ).values(
            'gender'
        ).annotate(
            count=Count('id')
        )
        
        return Response({
            'total': total,
            'active': active,
            'alumni': alumni,
            'class_distribution': class_distribution,
            'gender_distribution': gender_distribution
        })

class ParentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Parent CRUD operations
    """
    queryset = Parent.objects.all().select_related('user').prefetch_related('students')
    serializer_class = ParentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_primary', 'can_receive_sms', 'can_receive_email']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'occupation']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by user role
        user = self.request.user
        if user.has_role('teacher'):
            # Teachers see parents of their students
            teacher = user.teacher_profile
            if teacher:
                queryset = queryset.filter(
                    students__current_class__in=teacher.classes.all()
                ).distinct()
        elif user.has_role('student'):
            # Students see their own parents
            student = user.student_profile
            if student:
                queryset = queryset.filter(students=student)
        
        return queryset
    
    def perform_create(self, serializer):
        parent = serializer.save()
        
        AuditLog.objects.create(
            user=self.request.user,
            action='CREATE',
            model_name='Parent',
            object_id=str(parent.id),
            changes=ParentSerializer(parent).data,
            ip_address=self.request.META.get('REMOTE_ADDR', '')
        )
    
    def perform_update(self, serializer):
        old_data = ParentSerializer(self.get_object()).data
        parent = serializer.save()
        
        AuditLog.objects.create(
            user=self.request.user,
            action='UPDATE',
            model_name='Parent',
            object_id=str(parent.id),
            changes={'old': old_data, 'new': ParentSerializer(parent).data},
            ip_address=self.request.META.get('REMOTE_ADDR', '')
        )
    
    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        """Get all students of a parent"""
        parent = self.get_object()
        students = parent.students.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_student(self, request, pk=None):
        """Add a student to this parent"""
        parent = self.get_object()
        student_id = request.data.get('student_id')
        
        try:
            student = Student.objects.get(id=student_id)
            parent.students.add(student)
            
            AuditLog.objects.create(
                user=request.user,
                action='UPDATE',
                model_name='Parent',
                object_id=str(parent.id),
                changes={'added_student': student_id},
                ip_address=request.META.get('REMOTE_ADDR', '')
            )
            
            return Response({'message': 'Student added successfully'})
        except Student.DoesNotExist:
            return Response(
                {'error': 'Student not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def remove_student(self, request, pk=None):
        """Remove a student from this parent"""
        parent = self.get_object()
        student_id = request.data.get('student_id')
        
        try:
            student = Student.objects.get(id=student_id)
            parent.students.remove(student)
            
            AuditLog.objects.create(
                user=request.user,
                action='UPDATE',
                model_name='Parent',
                object_id=str(parent.id),
                changes={'removed_student': student_id},
                ip_address=request.META.get('REMOTE_ADDR', '')
            )
            
            return Response({'message': 'Student removed successfully'})
        except Student.DoesNotExist:
            return Response(
                {'error': 'Student not found'},
                status=status.HTTP_404_NOT_FOUND
            )

class StudentDocumentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Student Document CRUD operations
    """
    queryset = StudentDocument.objects.all().select_related('student', 'verified_by')
    serializer_class = StudentDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['student', 'document_type', 'verified']
    
    def perform_create(self, serializer):
        document = serializer.save()
        
        AuditLog.objects.create(
            user=self.request.user,
            action='CREATE',
            model_name='StudentDocument',
            object_id=str(document.id),
            changes=StudentDocumentSerializer(document).data,
            ip_address=self.request.META.get('REMOTE_ADDR', '')
        )
    
    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        """Verify a student document"""
        document = self.get_object()
        
        if document.verified:
            return Response(
                {'error': 'Document already verified'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        document.verified = True
        document.verified_by = request.user
        document.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='UPDATE',
            model_name='StudentDocument',
            object_id=str(document.id),
            changes={'verified': True, 'verified_by': request.user.id},
            ip_address=request.META.get('REMOTE_ADDR', '')
        )
        
        serializer = self.get_serializer(document)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def unverify(self, request, pk=None):
        """Unverify a student document"""
        document = self.get_object()
        
        document.verified = False
        document.verified_by = None
        document.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='UPDATE',
            model_name='StudentDocument',
            object_id=str(document.id),
            changes={'verified': False},
            ip_address=request.META.get('REMOTE_ADDR', '')
        )
        
        serializer = self.get_serializer(document)
        return Response(serializer.data)

class StudentPromotionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing student promotion history
    """
    queryset = StudentPromotion.objects.all().select_related(
        'student__user', 'from_class', 'to_class', 
        'from_section', 'to_section', 'academic_year', 'promoted_by'
    ).order_by('-promoted_on')
    
    serializer_class = StudentPromotionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['student', 'academic_year']