from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from django.utils import timezone
from .models import AcademicYear, Class, Section, Subject, Timetable
from .serializers import (
    AcademicYearSerializer, ClassSerializer, SectionSerializer,
    SubjectSerializer, TimetableSerializer, TimetableBulkSerializer
)
from accounts.models import AuditLog

class AcademicYearViewSet(viewsets.ModelViewSet):
    queryset = AcademicYear.objects.all().order_by('-start_date')
    serializer_class = AcademicYearSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['name']
    
    def perform_create(self, serializer):
        year = serializer.save()
        AuditLog.objects.create(
            user=self.request.user,
            action='CREATE',
            model_name='AcademicYear',
            object_id=str(year.id),
            changes=AcademicYearSerializer(year).data,
            ip_address=self.request.META.get('REMOTE_ADDR', '')
        )
    
    @action(detail=True, methods=['post'])
    def set_active(self, request, pk=None):
        year = self.get_object()
        AcademicYear.objects.exclude(id=year.id).update(is_active=False)
        year.is_active = True
        year.save()
        return Response({'message': f'{year.name} is now active'})

class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all().prefetch_related('sections').order_by('display_order')
    serializer_class = ClassSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'code']
    
    @action(detail=True, methods=['get'])
    def sections(self, request, pk=None):
        class_obj = self.get_object()
        sections = class_obj.sections.filter(is_active=True)
        serializer = SectionSerializer(sections, many=True)
        return Response(serializer.data)

class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all().select_related('class_group').order_by(
        'class_group__display_order', 'name'
    )
    serializer_class = SectionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['class_group', 'is_active']

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all().prefetch_related('classes').order_by('name')
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['subject_type', 'is_active', 'classes']
    search_fields = ['name', 'code']

class TimetableViewSet(viewsets.ModelViewSet):
    queryset = Timetable.objects.all().select_related(
        'class_group', 'section', 'subject', 'academic_year'
    ).order_by('day', 'start_time')
    
    serializer_class = TimetableSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'class_group': ['exact'],
        'section': ['exact'],
        'day': ['exact'],
        'academic_year': ['exact'],
        'is_active': ['exact'],
    }
    
    def perform_create(self, serializer):
        timetable = serializer.save()
        AuditLog.objects.create(
            user=self.request.user,
            action='CREATE',
            model_name='Timetable',
            object_id=str(timetable.id),
            changes=TimetableSerializer(timetable).data,
            ip_address=self.request.META.get('REMOTE_ADDR', '')
        )
    
    @action(detail=False, methods=['get'])
    def teacher_timetable(self, request):
        teacher_id = request.query_params.get('teacher_id')
        if not teacher_id:
            return Response(
                {'error': 'teacher_id required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        timetables = self.queryset.filter(
            teacher_id=teacher_id,
            is_active=True
        ).order_by('day', 'start_time')
        
        serializer = self.get_serializer(timetables, many=True)
        return Response(serializer.data)