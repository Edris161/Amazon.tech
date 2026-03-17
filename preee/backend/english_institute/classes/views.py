"""
Classes views module.
Handles API endpoints for Class and Enrollment management.
"""

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Class, Enrollment
from .serializers import ClassSerializer, EnrollmentSerializer

class ClassViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Class model.
    
    Provides comprehensive class management endpoints.
    
    Endpoints:
    - GET /classes/ - List all classes (with pagination, filtering)
    - POST /classes/ - Create new class
    - GET /classes/{id}/ - Retrieve class details
    - PUT /classes/{id}/ - Update class
    - DELETE /classes/{id}/ - Delete class
    - GET /classes/active/ - List active classes
    - GET /classes/{id}/enrollments/ - Get class enrollments
    - POST /classes/{id}/enroll/ - Enroll student in class
    """
    
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['level', 'is_active', 'teacher_name']
    search_fields = ['name', 'teacher_name', 'description']
    ordering_fields = ['start_date', 'name', 'capacity']
    ordering = ['-start_date']
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Get only active classes.
        """
        active_classes = self.queryset.filter(is_active=True)
        page = self.paginate_queryset(active_classes)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(active_classes, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def enrollments(self, request, pk=None):
        """
        Get all enrollments for a specific class.
        """
        class_obj = self.get_object()
        enrollments = class_obj.enrollments.all()
        
        page = self.paginate_queryset(enrollments)
        if page is not None:
            serializer = EnrollmentSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def enroll(self, request, pk=None):
        """
        Enroll a student in this class.
        """
        class_obj = self.get_object()
        student_id = request.data.get('student_id')
        
        from students.models import Student
        
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return Response(
                {'error': 'Student not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if already enrolled
        if Enrollment.objects.filter(student=student, class_enrolled=class_obj).exists():
            return Response(
                {'error': 'Student already enrolled in this class'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create enrollment
        enrollment_data = {
            'student': student.id,
            'class_enrolled': class_obj.id,
            'status': 'waitlisted' if class_obj.is_full else 'enrolled'
        }
        
        serializer = EnrollmentSerializer(data=enrollment_data)
        if serializer.is_valid():
            serializer.save()
            status_msg = "waitlisted" if class_obj.is_full else "enrolled"
            return Response({
                'message': f'Student successfully {status_msg} in class',
                'enrollment': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EnrollmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Enrollment model.
    
    Provides enrollment management endpoints.
    
    Endpoints:
    - GET /enrollments/ - List all enrollments
    - POST /enrollments/ - Create new enrollment
    - GET /enrollments/{id}/ - Retrieve enrollment
    - PUT /enrollments/{id}/ - Update enrollment
    - DELETE /enrollments/{id}/ - Delete enrollment
    - POST /enrollments/{id}/complete/ - Mark enrollment as completed
    - POST /enrollments/{id}/drop/ - Drop student from class
    """
    
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'student', 'class_enrolled']
    search_fields = ['student__first_name', 'student__last_name', 'class_enrolled__name']
    ordering_fields = ['enrollment_date', 'status']
    ordering = ['-enrollment_date']
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """
        Mark enrollment as completed.
        """
        enrollment = self.get_object()
        enrollment.status = 'completed'
        enrollment.save()
        
        return Response({
            'message': 'Enrollment marked as completed',
            'status': enrollment.status
        })
    
    @action(detail=True, methods=['post'])
    def drop(self, request, pk=None):
        """
        Drop student from class.
        """
        enrollment = self.get_object()
        enrollment.status = 'dropped'
        enrollment.save()
        
        return Response({
            'message': 'Student dropped from class',
            'status': enrollment.status
        })