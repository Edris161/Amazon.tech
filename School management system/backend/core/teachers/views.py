from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Sum
from django.utils import timezone
from datetime import timedelta
from .models import Teacher, TeacherAttendance, TeacherLeave
from .serializers import (
    TeacherSerializer, TeacherAttendanceSerializer,
    TeacherLeaveSerializer, TeacherBulkAttendanceSerializer
)
from accounts.models import User, AuditLog
from academics.models import Subject

class TeacherViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Teacher CRUD operations
    """
    queryset = Teacher.objects.all().select_related(
        'user'
    ).prefetch_related(
        'subjects', 'attendances', 'leaves'
    ).order_by('-joining_date')
    
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'employment_type': ['exact'],
        'qualification': ['exact'],
        'is_active': ['exact'],
        'gender': ['exact'],
        'joining_date': ['gte', 'lte', 'exact'],
        'leaving_date': ['gte', 'lte', 'exact'],
    }
    search_fields = [
        'user__first_name', 'user__last_name', 'user__email',
        'employee_id', 'user__phone', 'specialization'
    ]
    ordering_fields = [
        'employee_id', 'user__first_name', 'joining_date',
        'base_salary', 'experience_years'
    ]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by user role
        user = self.request.user
        if user.has_role('teacher'):
            # Teachers see only themselves
            teacher = user.teacher_profile
            if teacher:
                queryset = queryset.filter(id=teacher.id)
        elif user.has_role('student'):
            # Students see teachers of their class
            student = user.student_profile
            if student:
                queryset = queryset.filter(
                    subjects__classes=student.current_class
                ).distinct()
        
        return queryset
    
    def perform_create(self, serializer):
        teacher = serializer.save()
        
        AuditLog.objects.create(
            user=self.request.user,
            action='CREATE',
            model_name='Teacher',
            object_id=str(teacher.id),
            changes=TeacherSerializer(teacher).data,
            ip_address=self.request.META.get('REMOTE_ADDR', '')
        )
    
    def perform_update(self, serializer):
        old_data = TeacherSerializer(self.get_object()).data
        teacher = serializer.save()
        
        AuditLog.objects.create(
            user=self.request.user,
            action='UPDATE',
            model_name='Teacher',
            object_id=str(teacher.id),
            changes={'old': old_data, 'new': TeacherSerializer(teacher).data},
            ip_address=self.request.META.get('REMOTE_ADDR', '')
        )
    
    def perform_destroy(self, instance):
        AuditLog.objects.create(
            user=self.request.user,
            action='DELETE',
            model_name='Teacher',
            object_id=str(instance.id),
            changes={'employee_id': instance.employee_id},
            ip_address=self.request.META.get('REMOTE_ADDR', '')
        )
        instance.delete()
    
    @action(detail=True, methods=['get'])
    def attendance(self, request, pk=None):
        """Get attendance records for a teacher"""
        teacher = self.get_object()
        
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        month = request.query_params.get('month')
        year = request.query_params.get('year')
        
        attendances = teacher.attendances.all()
        
        if month and year:
            attendances = attendances.filter(
                date__year=year,
                date__month=month
            )
        elif start_date and end_date:
            attendances = attendances.filter(
                date__range=[start_date, end_date]
            )
        
        attendances = attendances.order_by('-date')
        serializer = TeacherAttendanceSerializer(attendances, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def leaves(self, request, pk=None):
        """Get leave records for a teacher"""
        teacher = self.get_object()
        
        status_filter = request.query_params.get('status')
        year = request.query_params.get('year', timezone.now().year)
        
        leaves = teacher.leaves.filter(from_date__year=year)
        
        if status_filter:
            leaves = leaves.filter(status=status_filter)
        
        leaves = leaves.order_by('-from_date')
        serializer = TeacherLeaveSerializer(leaves, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def subjects(self, request, pk=None):
        """Get subjects taught by a teacher"""
        teacher = self.get_object()
        subjects = teacher.subjects.all()
        from academics.serializers import SubjectSerializer
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def assign_subjects(self, request, pk=None):
        """Assign subjects to a teacher"""
        teacher = self.get_object()
        subject_ids = request.data.get('subject_ids', [])
        
        if not subject_ids:
            return Response(
                {'error': 'subject_ids required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        subjects = Subject.objects.filter(id__in=subject_ids)
        old_subjects = list(teacher.subjects.values_list('id', flat=True))
        teacher.subjects.set(subjects)
        
        AuditLog.objects.create(
            user=request.user,
            action='UPDATE',
            model_name='Teacher',
            object_id=str(teacher.id),
            changes={'old_subjects': old_subjects, 'new_subjects': subject_ids},
            ip_address=request.META.get('REMOTE_ADDR', '')
        )
        
        return Response(TeacherSerializer(teacher).data)
    
    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """Toggle teacher active status"""
        teacher = self.get_object()
        teacher.is_active = not teacher.is_active
        
        if not teacher.is_active:
            teacher.leaving_date = timezone.now().date()
        
        teacher.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='UPDATE',
            model_name='Teacher',
            object_id=str(teacher.id),
            changes={'is_active': teacher.is_active},
            ip_address=request.META.get('REMOTE_ADDR', '')
        )
        
        return Response({'is_active': teacher.is_active})
    
    @action(detail=True, methods=['post'])
    def mark_attendance(self, request, pk=None):
        """Mark attendance for a teacher"""
        teacher = self.get_object()
        date = request.data.get('date', timezone.now().date())
        status_value = request.data.get('status')
        check_in = request.data.get('check_in')
        check_out = request.data.get('check_out')
        remarks = request.data.get('remarks', '')
        
        if not status_value:
            return Response(
                {'error': 'status required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        attendance, created = TeacherAttendance.objects.update_or_create(
            teacher=teacher,
            date=date,
            defaults={
                'status': status_value,
                'check_in': check_in,
                'check_out': check_out,
                'remarks': remarks,
                'marked_by': request.user
            }
        )
        
        serializer = TeacherAttendanceSerializer(attendance)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get teacher statistics"""
        total = Teacher.objects.count()
        active = Teacher.objects.filter(is_active=True).count()
        
        employment_distribution = Teacher.objects.values(
            'employment_type'
        ).annotate(
            count=Count('id')
        )
        
        qualification_distribution = Teacher.objects.values(
            'qualification'
        ).annotate(
            count=Count('id')
        )
        
        subject_distribution = Teacher.objects.values(
            'subjects__name'
        ).annotate(
            count=Count('id')
        ).order_by('-count')[:10]
        
        # Today's attendance
        today = timezone.now().date()
        today_attendance = TeacherAttendance.objects.filter(
            date=today
        ).values(
            'status'
        ).annotate(
            count=Count('id')
        )
        
        return Response({
            'total': total,
            'active': active,
            'employment_distribution': employment_distribution,
            'qualification_distribution': qualification_distribution,
            'subject_distribution': subject_distribution,
            'today_attendance': today_attendance
        })

class TeacherAttendanceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Teacher Attendance CRUD operations
    """
    queryset = TeacherAttendance.objects.all().select_related(
        'teacher__user', 'marked_by'
    ).order_by('-date')
    
    serializer_class = TeacherAttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        'teacher': ['exact'],
        'date': ['exact', 'gte', 'lte'],
        'status': ['exact'],
        'marked_by': ['exact'],
    }
    ordering_fields = ['date', 'check_in', 'check_out']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by user role
        user = self.request.user
        if user.has_role('teacher'):
            teacher = user.teacher_profile
            if teacher:
                queryset = queryset.filter(teacher=teacher)
        
        return queryset
    
    def perform_create(self, serializer):
        attendance = serializer.save(marked_by=self.request.user)
        
        AuditLog.objects.create(
            user=self.request.user,
            action='CREATE',
            model_name='TeacherAttendance',
            object_id=str(attendance.id),
            changes=TeacherAttendanceSerializer(attendance).data,
            ip_address=self.request.META.get('REMOTE_ADDR', '')
        )
    
    @action(detail=False, methods=['post'])
    def bulk_mark(self, request):
        """Mark attendance for multiple teachers"""
        serializer = TeacherBulkAttendanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        date = serializer.validated_data['date']
        attendance_data = serializer.validated_data['attendance_data']
        
        created = []
        updated = []
        
        for item in attendance_data:
            teacher_id = item['teacher_id']
            status_value = item['status']
            remarks = item.get('remarks', '')
            
            try:
                teacher = Teacher.objects.get(id=teacher_id)
                
                attendance, is_created = TeacherAttendance.objects.update_or_create(
                    teacher=teacher,
                    date=date,
                    defaults={
                        'status': status_value,
                        'remarks': remarks,
                        'marked_by': request.user
                    }
                )
                
                if is_created:
                    created.append(teacher_id)
                else:
                    updated.append(teacher_id)
                    
            except Teacher.DoesNotExist:
                continue
        
        AuditLog.objects.create(
            user=request.user,
            action='CREATE',
            model_name='TeacherAttendance',
            object_id='bulk',
            changes={'date': str(date), 'created': created, 'updated': updated},
            ip_address=request.META.get('REMOTE_ADDR', '')
        )
        
        return Response({
            'message': f'Attendance marked for {len(created)} teachers, updated for {len(updated)} teachers',
            'created': created,
            'updated': updated
        })
    
    @action(detail=False, methods=['get'])
    def report(self, request):
        """Get attendance report"""
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        teacher_id = request.query_params.get('teacher_id')
        
        if not start_date or not end_date:
            return Response(
                {'error': 'start_date and end_date required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        attendances = TeacherAttendance.objects.filter(
            date__range=[start_date, end_date]
        )
        
        if teacher_id:
            attendances = attendances.filter(teacher_id=teacher_id)
        
        total_days = attendances.values('date').distinct().count()
        
        summary = attendances.values('status').annotate(
            count=Count('id'),
            teachers=Count('teacher', distinct=True)
        )
        
        daily_summary = attendances.values('date').annotate(
            present=Count('id', filter=models.Q(status='present')),
            absent=Count('id', filter=models.Q(status='absent')),
            late=Count('id', filter=models.Q(status='late')),
            leave=Count('id', filter=models.Q(status='leave'))
        ).order_by('date')
        
        return Response({
            'period': {'start': start_date, 'end': end_date},
            'total_days': total_days,
            'summary': summary,
            'daily_summary': daily_summary
        })

class TeacherLeaveViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Teacher Leave CRUD operations
    """
    queryset = TeacherLeave.objects.all().select_related(
        'teacher__user', 'approved_by'
    ).order_by('-from_date')
    
    serializer_class = TeacherLeaveSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        'teacher': ['exact'],
        'leave_type': ['exact'],
        'status': ['exact'],
        'from_date': ['gte', 'lte'],
        'to_date': ['gte', 'lte'],
    }
    search_fields = ['teacher__user__first_name', 'teacher__user__last_name', 'reason']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by user role
        user = self.request.user
        if user.has_role('teacher'):
            teacher = user.teacher_profile
            if teacher:
                queryset = queryset.filter(teacher=teacher)
        
        return queryset
    
    def perform_create(self, serializer):
        leave = serializer.save()
        
        AuditLog.objects.create(
            user=self.request.user,
            action='CREATE',
            model_name='TeacherLeave',
            object_id=str(leave.id),
            changes=TeacherLeaveSerializer(leave).data,
            ip_address=self.request.META.get('REMOTE_ADDR', '')
        )
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve leave request"""
        leave = self.get_object()
        
        if leave.status != 'pending':
            return Response(
                {'error': f'Leave is already {leave.status}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        leave.status = 'approved'
        leave.approved_by = request.user
        leave.approved_on = timezone.now()
        leave.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='UPDATE',
            model_name='TeacherLeave',
            object_id=str(leave.id),
            changes={'status': 'approved'},
            ip_address=request.META.get('REMOTE_ADDR', '')
        )
        
        serializer = self.get_serializer(leave)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject leave request"""
        leave = self.get_object()
        
        if leave.status != 'pending':
            return Response(
                {'error': f'Leave is already {leave.status}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        remarks = request.data.get('remarks', '')
        
        leave.status = 'rejected'
        leave.remarks = remarks
        leave.approved_by = request.user
        leave.approved_on = timezone.now()
        leave.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='UPDATE',
            model_name='TeacherLeave',
            object_id=str(leave.id),
            changes={'status': 'rejected', 'remarks': remarks},
            ip_address=request.META.get('REMOTE_ADDR', '')
        )
        
        serializer = self.get_serializer(leave)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel leave request"""
        leave = self.get_object()
        
        if leave.status not in ['pending', 'approved']:
            return Response(
                {'error': f'Cannot cancel leave with status {leave.status}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        leave.status = 'cancelled'
        leave.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='UPDATE',
            model_name='TeacherLeave',
            object_id=str(leave.id),
            changes={'status': 'cancelled'},
            ip_address=request.META.get('REMOTE_ADDR', '')
        )
        
        serializer = self.get_serializer(leave)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get leave statistics"""
        year = request.query_params.get('year', timezone.now().year)
        
        leaves = TeacherLeave.objects.filter(from_date__year=year)
        
        by_type = leaves.values('leave_type').annotate(
            total_days=Sum('days_count'),
            count=Count('id'),
            approved=Count('id', filter=models.Q(status='approved')),
            pending=Count('id', filter=models.Q(status='pending'))
        )
        
        by_month = leaves.values(
            month=models.functions.ExtractMonth('from_date')
        ).annotate(
            total_days=Sum('days_count'),
            count=Count('id')
        ).order_by('month')
        
        by_teacher = leaves.values(
            'teacher__user__first_name',
            'teacher__user__last_name'
        ).annotate(
            total_days=Sum('days_count'),
            count=Count('id')
        ).order_by('-total_days')[:10]
        
        return Response({
            'year': year,
            'by_type': by_type,
            'by_month': by_month,
            'top_teachers': by_teacher
        })