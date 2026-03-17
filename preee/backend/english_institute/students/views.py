"""
Students views module.
Handles API endpoints for Student and Level management.
"""

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Student, Level
from .serializers import StudentSerializer, LevelSerializer

class LevelViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Level model.
    
    Provides CRUD operations for English levels.
    
    Endpoints:
    - GET /levels/ - List all levels
    - POST /levels/ - Create new level
    - GET /levels/{id}/ - Retrieve level
    - PUT /levels/{id}/ - Update level
    - DELETE /levels/{id}/ - Delete level
    """
    
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code']
    ordering_fields = ['order', 'name']

class StudentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Student model.
    
    Provides comprehensive student management endpoints.
    
    Endpoints:
    - GET /students/ - List all students (with pagination, filtering)
    - POST /students/ - Register new student
    - GET /students/{id}/ - Retrieve student details
    - PUT /students/{id}/ - Update student
    - PATCH /students/{id}/ - Partial update student
    - DELETE /students/{id}/ - Delete student
    - GET /students/search/?q= - Search students
    - GET /students/active/ - List active students
    - POST /students/{id}/toggle_status/ - Activate/deactivate student
    """
    
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['level', 'is_active']
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'student_id']
    ordering_fields = ['registration_date', 'last_name', 'first_name']
    ordering = ['-registration_date']
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Get only active students.
        """
        active_students = self.queryset.filter(is_active=True)
        page = self.paginate_queryset(active_students)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(active_students, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        """
        Toggle student active status.
        """
        student = self.get_object()
        student.is_active = not student.is_active
        student.save()
        
        status_text = "activated" if student.is_active else "deactivated"
        return Response({
            'message': f'Student {status_text} successfully',
            'is_active': student.is_active
        })
    
    @action(detail=True, methods=['get'])
    def enrollments(self, request, pk=None):
        """
        Get all enrollments for a specific student.
        """
        student = self.get_object()
        enrollments = student.enrollments.all()
        
        from classes.serializers import EnrollmentSerializer
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)