from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Sum, Avg, Max, Min
from django.db.models.functions import TruncMonth
from django.utils import timezone
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import io
import csv
from .models import Exam, ExamSchedule, ExamResult, ReportCard
from .serializers import (
    ExamSerializer, ExamScheduleSerializer, ExamResultSerializer,
    ExamResultBulkSerializer, ReportCardSerializer, ExamResultSummarySerializer
)
from students.models import Student
from accounts.models import AuditLog

class ExamViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Exam CRUD operations
    """
    queryset = Exam.objects.all().select_related(
        'class_group', 'academic_year', 'created_by'
    ).prefetch_related('schedules').order_by('-start_date')
    
    serializer_class = ExamSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'class_group': ['exact'],
        'academic_year': ['exact'],
        'exam_type': ['exact'],
        'is_published': ['exact'],
        'start_date': ['gte', 'lte'],
        'end_date': ['gte', 'lte'],
    }
    search_fields = ['name', 'description']
    ordering_fields = ['start_date', 'name', 'created_at']
    
    def perform_create(self, serializer):
        exam = serializer.save()
        
        AuditLog.objects.create(
            user=self.request.user,
            action='CREATE',
            model_name='Exam',
            object_id=str(exam.id),
            changes=ExamSerializer(exam).data,
            ip_address=self.request.META.get('REMOTE_ADDR', '')
        )
    
    @action(detail=True, methods=['get'])
    def schedules(self, request, pk=None):
        """Get exam schedules"""
        exam = self.get_object()
        schedules = exam.schedules.all().select_related('subject').order_by('date', 'start_time')
        serializer = ExamScheduleSerializer(schedules, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        """Get exam results"""
        exam = self.get_object()
        results = ExamResult.objects.filter(
            exam_schedule__exam=exam
        ).select_related(
            'student__user', 'exam_schedule__subject'
        ).order_by('student__roll_number')
        
        serializer = ExamResultSerializer(results, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        """Get exam summary statistics"""
        exam = self.get_object()
        
        # Get all results for this exam
        results = ExamResult.objects.filter(
            exam_schedule__exam=exam
        ).select_related('student', 'exam_schedule__subject')
        
        # Overall statistics
        total_students = results.values('student').distinct().count()
        total_subjects = exam.schedules.count()
        
        # Subject-wise statistics
        subject_stats = []
        for schedule in exam.schedules.all():
            subject_results = results.filter(exam_schedule=schedule)
            if subject_results.exists():
                subject_stats.append({
                    'subject': schedule.subject.name,
                    'max_marks': schedule.max_marks,
                    'pass_marks': schedule.pass_marks,
                    'total_students': subject_results.count(),
                    'highest': subject_results.aggregate(Max('marks_obtained'))['marks_obtained__max'],
                    'lowest': subject_results.aggregate(Min('marks_obtained'))['marks_obtained__min'],
                    'average': round(subject_results.aggregate(Avg('marks_obtained'))['marks_obtained__avg'], 2),
                    'pass_count': subject_results.filter(marks_obtained__gte=schedule.pass_marks).count(),
                })
        
        # Grade distribution
        grade_distribution = results.values('grade').annotate(
            count=Count('id')
        ).order_by('grade')
        
        return Response({
            'exam_id': exam.id,
            'exam_name': exam.name,
            'total_students': total_students,
            'total_subjects': total_subjects,
            'subject_statistics': subject_stats,
            'grade_distribution': grade_distribution
        })
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """Publish exam results"""
        exam = self.get_object()
        exam.is_published = True
        exam.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='UPDATE',
            model_name='Exam',
            object_id=str(exam.id),
            changes={'is_published': True},
            ip_address=request.META.get('REMOTE_ADDR', '')
        )
        
        return Response({'message': 'Exam results published successfully'})
    
    @action(detail=True, methods=['post'])
    def unpublish(self, request, pk=None):
        """Unpublish exam results"""
        exam = self.get_object()
        exam.is_published = False
        exam.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='UPDATE',
            model_name='Exam',
            object_id=str(exam.id),
            changes={'is_published': False},
            ip_address=request.META.get('REMOTE_ADDR', '')
        )
        
        return Response({'message': 'Exam results unpublished successfully'})

class ExamScheduleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Exam Schedule CRUD operations
    """
    queryset = ExamSchedule.objects.all().select_related(
        'exam', 'subject'
    ).order_by('date', 'start_time')
    
    serializer_class = ExamScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['exam', 'subject', 'date']
    
    def perform_create(self, serializer):
        schedule = serializer.save()
        
        AuditLog.objects.create(
            user=self.request.user,
            action='CREATE',
            model_name='ExamSchedule',
            object_id=str(schedule.id),
            changes=ExamScheduleSerializer(schedule).data,
            ip_address=self.request.META.get('REMOTE_ADDR', '')
        )
    
    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        """Get results for this schedule"""
        schedule = self.get_object()
        results = schedule.results.all().select_related('student__user').order_by('student__roll_number')
        serializer = ExamResultSerializer(results, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def enter_marks(self, request, pk=None):
        """Enter marks for all students in this schedule"""
        schedule = self.get_object()
        marks_data = request.data.get('marks', [])
        
        created = []
        updated = []
        
        for item in marks_data:
            student_id = item.get('student_id')
            marks = item.get('marks_obtained')
            
            try:
                result, is_created = ExamResult.objects.update_or_create(
                    exam_schedule=schedule,
                    student_id=student_id,
                    defaults={
                        'marks_obtained': marks,
                        'entered_by': request.user.teacher_profile
                    }
                )
                
                if is_created:
                    created.append(student_id)
                else:
                    updated.append(student_id)
                    
            except Exception as e:
                continue
        
        AuditLog.objects.create(
            user=request.user,
            action='CREATE',
            model_name='ExamResult',
            object_id='bulk',
            changes={
                'exam_schedule': schedule.id,
                'created': len(created),
                'updated': len(updated)
            },
            ip_address=request.META.get('REMOTE_ADDR', '')
        )
        
        return Response({
            'message': f'Marks entered for {len(created)} students, updated for {len(updated)} students',
            'created': created,
            'updated': updated
        })

class ExamResultViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Exam Result CRUD operations
    """
    queryset = ExamResult.objects.all().select_related(
        'exam_schedule__exam', 'exam_schedule__subject', 'student__user', 'entered_by__user'
    ).order_by('student__roll_number')
    
    serializer_class = ExamResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        'exam_schedule': ['exact'],
        'student': ['exact'],
        'exam_schedule__exam': ['exact'],
        'exam_schedule__subject': ['exact'],
        'grade': ['exact'],
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
        result = serializer.save()
        
        AuditLog.objects.create(
            user=self.request.user,
            action='CREATE',
            model_name='ExamResult',
            object_id=str(result.id),
            changes=ExamResultSerializer(result).data,
            ip_address=self.request.META.get('REMOTE_ADDR', '')
        )
    
    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """Create multiple exam results at once"""
        serializer = ExamResultBulkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        exam_schedule_id = data['exam_schedule_id']
        results_data = data['results']
        
        try:
            exam_schedule = ExamSchedule.objects.get(id=exam_schedule_id)
        except ExamSchedule.DoesNotExist:
            return Response(
                {'error': 'Exam schedule not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        created = []
        errors = []
        
        for item in results_data:
            try:
                result, is_created = ExamResult.objects.update_or_create(
                    exam_schedule=exam_schedule,
                    student_id=item['student_id'],
                    defaults={
                        'marks_obtained': item['marks_obtained'],
                        'remarks': item.get('remarks', ''),
                        'entered_by': request.user.teacher_profile
                    }
                )
                
                created.append({
                    'student_id': item['student_id'],
                    'marks': item['marks_obtained'],
                    'grade': result.grade
                })
                
            except Exception as e:
                errors.append({
                    'student_id': item['student_id'],
                    'error': str(e)
                })
        
        AuditLog.objects.create(
            user=request.user,
            action='CREATE',
            model_name='ExamResult',
            object_id='bulk',
            changes={
                'exam_schedule': exam_schedule_id,
                'created': len(created),
                'errors': len(errors)
            },
            ip_address=request.META.get('REMOTE_ADDR', '')
        )
        
        return Response({
            'exam_schedule': exam_schedule_id,
            'created': created,
            'errors': errors
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def student_marksheet(self, request):
        """Get complete marksheet for a student"""
        student_id = request.query_params.get('student_id')
        exam_id = request.query_params.get('exam_id')
        
        if not student_id:
            return Response(
                {'error': 'student_id required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        results = self.queryset.filter(student_id=student_id)
        
        if exam_id:
            results = results.filter(exam_schedule__exam_id=exam_id)
        
        if not results.exists():
            return Response(
                {'error': 'No results found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Group by exam
        marksheet = {}
        for result in results:
            exam_name = result.exam_schedule.exam.name
            if exam_name not in marksheet:
                marksheet[exam_name] = {
                    'exam_id': result.exam_schedule.exam.id,
                    'subjects': []
                }
            
            marksheet[exam_name]['subjects'].append({
                'subject': result.exam_schedule.subject.name,
                'max_marks': result.exam_schedule.max_marks,
                'marks_obtained': result.marks_obtained,
                'grade': result.grade,
                'percentage': (result.marks_obtained / result.exam_schedule.max_marks) * 100
            })
        
        # Calculate totals and percentages
        for exam in marksheet.values():
            total_obtained = sum(s['marks_obtained'] for s in exam['subjects'])
            total_max = sum(s['max_marks'] for s in exam['subjects'])
            exam['total_obtained'] = total_obtained
            exam['total_max'] = total_max
            exam['overall_percentage'] = round((total_obtained / total_max) * 100, 2) if total_max > 0 else 0
        
        return Response({
            'student_id': student_id,
            'student_name': results.first().student.user.full_name,
            'marksheet': marksheet
        })

class ReportCardViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Report Card operations
    """
    queryset = ReportCard.objects.all().select_related(
        'student__user', 'exam', 'generated_by'
    ).order_by('-generated_at')
    
    serializer_class = ReportCardSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['student', 'exam', 'result']
    
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
    
    @action(detail=False, methods=['post'])
    def generate(self, request):
        """Generate report card for a student"""
        student_id = request.data.get('student_id')
        exam_id = request.data.get('exam_id')
        
        if not student_id or not exam_id:
            return Response(
                {'error': 'student_id and exam_id required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            student = Student.objects.get(id=student_id)
            exam = Exam.objects.get(id=exam_id)
        except (Student.DoesNotExist, Exam.DoesNotExist):
            return Response(
                {'error': 'Student or Exam not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get all results for this student in this exam
        results = ExamResult.objects.filter(
            student=student,
            exam_schedule__exam=exam
        ).select_related('exam_schedule__subject')
        
        if not results.exists():
            return Response(
                {'error': 'No results found for this student in this exam'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Calculate totals
        total_marks = sum(r.marks_obtained for r in results)
        total_max = sum(r.exam_schedule.max_marks for r in results)
        percentage = (total_marks / total_max) * 100 if total_max > 0 else 0
        
        # Determine grade
        if percentage >= 90:
            grade = 'A+'
            result = 'distinction'
        elif percentage >= 80:
            grade = 'A'
            result = 'distinction'
        elif percentage >= 70:
            grade = 'B+'
            result = 'pass'
        elif percentage >= 60:
            grade = 'B'
            result = 'pass'
        elif percentage >= 50:
            grade = 'C+'
            result = 'pass'
        elif percentage >= 40:
            grade = 'C'
            result = 'pass'
        else:
            grade = 'F'
            result = 'fail'
        
        # Calculate rank
        all_students_total = ExamResult.objects.filter(
            exam_schedule__exam=exam
        ).values('student').annotate(
            total=Sum('marks_obtained')
        ).order_by('-total')
        
        rank = 1
        for item in all_students_total:
            if item['student'] == student.id:
                break
            rank += 1
        
        # Create report card
        report_card = ReportCard.objects.create(
            student=student,
            exam=exam,
            total_marks=total_marks,
            percentage=percentage,
            grade=grade,
            rank=rank,
            result=result,
            generated_by=request.user
        )
        
        # Generate PDF (simplified - you would implement actual PDF generation)
        self.generate_pdf(report_card)
        
        serializer = self.get_serializer(report_card)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def generate_pdf(self, report_card):
        """Generate PDF for report card"""
        # This is a simplified version - you would implement full PDF generation
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        
        # Add content
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, 800, f"Report Card - {report_card.exam.name}")
        
        p.setFont("Helvetica", 12)
        p.drawString(100, 750, f"Student: {report_card.student.user.full_name}")
        p.drawString(100, 730, f"Class: {report_card.student.current_class.name}")
        p.drawString(100, 710, f"Section: {report_card.student.current_section.name}")
        p.drawString(100, 690, f"Roll Number: {report_card.student.roll_number}")
        
        p.drawString(100, 650, f"Total Marks: {report_card.total_marks}")
        p.drawString(100, 630, f"Percentage: {report_card.percentage}%")
        p.drawString(100, 610, f"Grade: {report_card.grade}")
        p.drawString(100, 590, f"Rank: {report_card.rank}")
        p.drawString(100, 570, f"Result: {report_card.result.upper()}")
        
        p.save()
        
        # Save PDF to file
        buffer.seek(0)
        filename = f"report_card_{report_card.student.admission_number}_{report_card.exam.id}.pdf"
        report_card.pdf_file.save(filename, buffer)
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """Download report card PDF"""
        report_card = self.get_object()
        
        if not report_card.pdf_file:
            return Response(
                {'error': 'PDF not generated yet'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Return file response
        from django.http import FileResponse
        return FileResponse(
            report_card.pdf_file.open(),
            as_attachment=True,
            filename=f"report_card_{report_card.student.admission_number}.pdf"
        )
    
    @action(detail=False, methods=['get'])
    def class_rankings(self, request):
        """Get class rankings for an exam"""
        exam_id = request.query_params.get('exam_id')
        class_id = request.query_params.get('class_id')
        
        if not exam_id:
            return Response(
                {'error': 'exam_id required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        results = ExamResult.objects.filter(
            exam_schedule__exam_id=exam_id
        ).select_related('student__user')
        
        if class_id:
            results = results.filter(student__current_class_id=class_id)
        
        # Calculate total marks per student
        student_totals = {}
        for result in results:
            student_id = result.student.id
            if student_id not in student_totals:
                student_totals[student_id] = {
                    'student_id': student_id,
                    'student_name': result.student.user.full_name,
                    'roll_number': result.student.roll_number,
                    'class': result.student.current_class.name,
                    'section': result.student.current_section.name,
                    'total_marks': 0,
                    'subjects': []
                }
            student_totals[student_id]['total_marks'] += result.marks_obtained
            student_totals[student_id]['subjects'].append({
                'subject': result.exam_schedule.subject.name,
                'marks': result.marks_obtained
            })
        
        # Sort by total marks and add rank
        rankings = sorted(
            student_totals.values(),
            key=lambda x: x['total_marks'],
            reverse=True
        )
        
        for i, item in enumerate(rankings, 1):
            item['rank'] = i
        
        return Response(rankings)