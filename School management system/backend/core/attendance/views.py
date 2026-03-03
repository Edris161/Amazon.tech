from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Sum, Case, When, IntegerField
from django.db.models.functions import TruncMonth, TruncWeek
from django.utils import timezone
from datetime import timedelta, datetime
import calendar
from .models import StudentAttendance, BulkAttendance, Holiday
from .serializers import (
    StudentAttendanceSerializer, BulkAttendanceSerializer,
    HolidaySerializer, DailyAttendanceSummarySerializer,
    MonthlyAttendanceReportSerializer
)
from students.models import Student
from academics.models import Class, Section, AcademicYear
from accounts.models import AuditLog

class StudentAttendanceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Student Attendance CRUD operations
    """
    queryset = StudentAttendance.objects.all().select_related(
        'student__user', 'class_group', 'section', 'marked_by'
    ).order_by('-date', 'student__roll_number')
    
    serializer_class = StudentAttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'student': ['exact'],
        'class_group': ['exact'],
        'section': ['exact'],
        'academic_year': ['exact'],
        'date': ['exact', 'gte', 'lte'],
        'status': ['exact'],
        'marked_by': ['exact'],
    }
    search_fields = ['student__user__first_name', 'student__user__last_name', 'remarks']
    ordering_fields = ['date', 'student__roll_number', 'marked_at']
    
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
        elif user.has_role('teacher'):
            teacher = user.teacher_profile
            if teacher:
                queryset = queryset.filter(
                    class_group__in=teacher.classes.all()
                )
        
        return queryset
    
    def perform_create(self, serializer):
        attendance = serializer.save()
        
        AuditLog.objects.create(
            user=self.request.user,
            action='CREATE',
            model_name='StudentAttendance',
            object_id=str(attendance.id),
            changes=StudentAttendanceSerializer(attendance).data,
            ip_address=self.request.META.get('REMOTE_ADDR', '')
        )
    
    @action(detail=False, methods=['post'])
    def mark_bulk(self, request):
        """Mark attendance for multiple students at once"""
        date = request.data.get('date', timezone.now().date())
        class_id = request.data.get('class_id')
        section_id = request.data.get('section_id')
        academic_year_id = request.data.get('academic_year_id')
        attendance_data = request.data.get('attendance_data', [])
        
        if not all([class_id, section_id, academic_year_id]):
            return Response(
                {'error': 'class_id, section_id, and academic_year_id required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if bulk attendance already exists
        bulk, created = BulkAttendance.objects.get_or_create(
            class_group_id=class_id,
            section_id=section_id,
            date=date,
            defaults={
                'attendance_data': attendance_data,
                'total_students': len(attendance_data),
                'marked_by': request.user
            }
        )
        
        if not created:
            bulk.attendance_data = attendance_data
            bulk.marked_by = request.user
            bulk.save()
        
        # Create individual attendance records
        created_count = 0
        updated_count = 0
        
        for item in attendance_data:
            student_id = item.get('student_id')
            status_value = item.get('status')
            remarks = item.get('remarks', '')
            
            try:
                attendance, is_created = StudentAttendance.objects.update_or_create(
                    student_id=student_id,
                    date=date,
                    defaults={
                        'class_group_id': class_id,
                        'section_id': section_id,
                        'academic_year_id': academic_year_id,
                        'status': status_value,
                        'remarks': remarks,
                        'marked_by': request.user
                    }
                )
                
                if is_created:
                    created_count += 1
                else:
                    updated_count += 1
                    
            except Student.DoesNotExist:
                continue
        
        # Update bulk record counts
        bulk.total_present = attendance_data.count(
            lambda x: x.get('status') in ['present', 'late']
        )
        bulk.total_absent = attendance_data.count(
            lambda x: x.get('status') == 'absent'
        )
        bulk.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='CREATE',
            model_name='StudentAttendance',
            object_id='bulk',
            changes={
                'date': str(date),
                'class_id': class_id,
                'section_id': section_id,
                'created': created_count,
                'updated': updated_count
            },
            ip_address=request.META.get('REMOTE_ADDR', '')
        )
        
        return Response({
            'message': f'Attendance marked for {created_count} students, updated for {updated_count} students',
            'bulk_id': bulk.id
        })
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get today's attendance"""
        date = request.query_params.get('date', timezone.now().date())
        class_id = request.query_params.get('class_id')
        section_id = request.query_params.get('section_id')
        
        attendances = StudentAttendance.objects.filter(date=date)
        
        if class_id:
            attendances = attendances.filter(class_group_id=class_id)
        if section_id:
            attendances = attendances.filter(section_id=section_id)
        
        # Check if it's a holiday
        try:
            holiday = Holiday.objects.get(date=date)
            return Response({
                'date': date,
                'is_holiday': True,
                'holiday_name': holiday.name,
                'holiday_type': holiday.holiday_type
            })
        except Holiday.DoesNotExist:
            pass
        
        attendances = attendances.select_related('student__user')
        serializer = self.get_serializer(attendances, many=True)
        
        # Get summary
        summary = attendances.values('status').annotate(
            count=Count('id')
        )
        
        return Response({
            'date': date,
            'is_holiday': False,
            'attendance': serializer.data,
            'summary': summary
        })
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get attendance summary"""
        class_id = request.query_params.get('class_id')
        section_id = request.query_params.get('section_id')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if not start_date:
            start_date = timezone.now().date().replace(day=1)
        if not end_date:
            end_date = timezone.now().date()
        
        attendances = StudentAttendance.objects.filter(
            date__range=[start_date, end_date]
        )
        
        if class_id:
            attendances = attendances.filter(class_group_id=class_id)
        if section_id:
            attendances = attendances.filter(section_id=section_id)
        
        # Daily summary
        daily = attendances.values('date').annotate(
            total=Count('id'),
            present=Count('id', filter=Q(status='present')),
            absent=Count('id', filter=Q(status='absent')),
            late=Count('id', filter=Q(status='late')),
            half_day=Count('id', filter=Q(status='half_day'))
        ).order_by('date')
        
        # Overall summary
        overall = attendances.aggregate(
            total=Count('id'),
            present=Count('id', filter=Q(status='present')),
            absent=Count('id', filter=Q(status='absent')),
            late=Count('id', filter=Q(status='late')),
            half_day=Count('id', filter=Q(status='half_day'))
        )
        
        # Calculate percentages
        if overall['total']:
            overall['present_percentage'] = round(
                (overall['present'] / overall['total']) * 100, 2
            )
        else:
            overall['present_percentage'] = 0
        
        return Response({
            'period': {'start': start_date, 'end': end_date},
            'daily': daily,
            'overall': overall
        })
    
    @action(detail=False, methods=['get'])
    def student_report(self, request):
        """Get attendance report for a specific student"""
        student_id = request.query_params.get('student_id')
        month = request.query_params.get('month')
        year = request.query_params.get('year')
        
        if not student_id:
            return Response(
                {'error': 'student_id required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        attendances = StudentAttendance.objects.filter(student_id=student_id)
        
        if month and year:
            attendances = attendances.filter(
                date__year=year,
                date__month=month
            )
        
        attendances = attendances.order_by('date')
        
        total_days = attendances.count()
        summary = attendances.values('status').annotate(count=Count('id'))
        
        # Calculate percentage
        present_count = attendances.filter(
            status__in=['present', 'late']
        ).count()
        
        percentage = round((present_count / total_days * 100), 2) if total_days > 0 else 0
        
        serializer = self.get_serializer(attendances, many=True)
        
        return Response({
            'student_id': student_id,
            'total_days': total_days,
            'attendance_percentage': percentage,
            'summary': summary,
            'records': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def class_report(self, request):
        """Get attendance report for a class"""
        class_id = request.query_params.get('class_id')
        section_id = request.query_params.get('section_id')
        month = request.query_params.get('month')
        year = request.query_params.get('year')
        
        if not class_id:
            return Response(
                {'error': 'class_id required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get all students in the class
        students = Student.objects.filter(
            current_class_id=class_id,
            is_active=True
        )
        
        if section_id:
            students = students.filter(current_section_id=section_id)
        
        students = students.order_by('roll_number')
        
        # Get attendance for the period
        attendances = StudentAttendance.objects.filter(
            student__in=students
        )
        
        if month and year:
            attendances = attendances.filter(
                date__year=year,
                date__month=month
            )
        
        # Calculate days in month
        if month and year:
            _, last_day = calendar.monthrange(int(year), int(month))
            total_days = last_day
        else:
            total_days = attendances.values('date').distinct().count()
        
        report = []
        for student in students:
            student_attendance = attendances.filter(student=student)
            present = student_attendance.filter(status='present').count()
            absent = student_attendance.filter(status='absent').count()
            late = student_attendance.filter(status='late').count()
            half_day = student_attendance.filter(status='half_day').count()
            
            total_present = present + late + (half_day * 0.5)
            percentage = round((total_present / total_days * 100), 2) if total_days > 0 else 0
            
            report.append({
                'student_id': student.id,
                'student_name': student.user.full_name,
                'roll_number': student.roll_number,
                'present': present,
                'absent': absent,
                'late': late,
                'half_day': half_day,
                'attendance_percentage': percentage
            })
        
        return Response({
            'class_id': class_id,
            'section_id': section_id,
            'month': month,
            'year': year,
            'total_days': total_days,
            'total_students': students.count(),
            'report': report
        })

class BulkAttendanceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing bulk attendance records
    """
    queryset = BulkAttendance.objects.all().select_related(
        'class_group', 'section', 'marked_by'
    ).order_by('-date')
    
    serializer_class = BulkAttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['class_group', 'section', 'date', 'marked_by']
    
    @action(detail=True, methods=['get'])
    def details(self, request, pk=None):
        """Get detailed attendance for this bulk record"""
        bulk = self.get_object()
        
        attendances = StudentAttendance.objects.filter(
            class_group=bulk.class_group,
            section=bulk.section,
            date=bulk.date
        ).select_related('student__user')
        
        serializer = StudentAttendanceSerializer(attendances, many=True)
        return Response(serializer.data)

class HolidayViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Holiday CRUD operations
    """
    queryset = Holiday.objects.all().select_related('class_group', 'academic_year').order_by('date')
    serializer_class = HolidaySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        'holiday_type': ['exact'],
        'date': ['exact', 'gte', 'lte'],
        'class_group': ['exact'],
        'academic_year': ['exact'],
        'is_recurring': ['exact'],
    }
    search_fields = ['name', 'description']
    
    def perform_create(self, serializer):
        holiday = serializer.save()
        
        AuditLog.objects.create(
            user=self.request.user,
            action='CREATE',
            model_name='Holiday',
            object_id=str(holiday.id),
            changes=HolidaySerializer(holiday).data,
            ip_address=self.request.META.get('REMOTE_ADDR', '')
        )
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming holidays"""
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now().date()
        end_date = start_date + timedelta(days=days)
        
        holidays = self.queryset.filter(
            date__range=[start_date, end_date]
        ).order_by('date')
        
        serializer = self.get_serializer(holidays, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def calendar(self, request):
        """Get holiday calendar for a year"""
        year = request.query_params.get('year', timezone.now().year)
        
        holidays = self.queryset.filter(
            date__year=year
        ).order_by('date')
        
        # Group by month
        calendar_data = {}
        for holiday in holidays:
            month = holiday.date.strftime('%B')
            if month not in calendar_data:
                calendar_data[month] = []
            calendar_data[month].append({
                'date': holiday.date,
                'name': holiday.name,
                'type': holiday.holiday_type
            })
        
        return Response(calendar_data)