from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Avg
from django.utils import timezone
from datetime import timedelta
from .models import Assignment, Submission
from .serializers import (
    AssignmentSerializer, SubmissionSerializer,
    SubmissionGradeSerializer, AssignmentBulkCreateSerializer
)
from students.models import Student
from teachers.models import Teacher
from accounts.models import AuditLog

class AssignmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Assignment CRUD operations
    """
    queryset = Assignment.objects.all().select_related(
        'class_group', 'section', 'subject', 'teacher__user'
    ).prefetch_related('submissions').order_by('-due_date')
    
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'class_group': ['exact'],
        'section': ['exact'],
        'subject': ['exact'],
        'teacher': ['exact'],
        'assignment_type': ['exact'],
        'is_published': ['exact'],
        'due_date': ['gte', 'lte'],
        'created_at': ['gte', 'lte'],
    }
    search_fields = ['title', 'description', 'instructions']
    ordering_fields = ['due_date', 'created_at', 'title']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by user role
        user = self.request.user
        if user.has_role('teacher'):
            teacher = user.teacher_profile
            if teacher:
                queryset = queryset.filter(teacher=teacher)
        elif user.has_role('student'):
            student = user.student_profile
            if student:
                queryset = queryset.filter(
                    class_group=student.current_class,
                    section=student.current_section
                )
        elif user.has_role('parent'):
            parent = user.parent_profile
            if parent:
                queryset = queryset.filter(
                    class_group__in=parent.students.values('current_class')
                ).distinct()
        
        return queryset
    
    def perform_create(self, serializer):
        assignment = serializer.save()
        
        AuditLog.objects.create(
            user=self.request.user,
            action='CREATE',
            model_name='Assignment',
            object_id=str(assignment.id),
            changes=AssignmentSerializer(assignment).data,
            ip_address=self.request.META.get('REMOTE_ADDR', '')
        )
    
    @action(detail=True, methods=['get'])
    def submissions(self, request, pk=None):
        """Get all submissions for this assignment"""
        assignment = self.get_object()
        submissions = assignment.submissions.all().select_related(
            'student__user', 'graded_by__user'
        ).order_by('student__roll_number')
        
        serializer = SubmissionSerializer(submissions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def submission_summary(self, request, pk=None):
        """Get submission summary for this assignment"""
        assignment = self.get_object()
        
        # Get all students in the class/section
        total_students = Student.objects.filter(
            current_class=assignment.class_group,
            current_section=assignment.section,
            is_active=True
        ).count()
        
        submissions = assignment.submissions.all()
        
        submitted_count = submissions.count()
        graded_count = submissions.filter(status='graded').count()
        pending_count = submissions.filter(status='submitted').count()
        late_count = submissions.filter(status='late').count()
        
        if graded_count > 0:
            average_marks = submissions.filter(
                status='graded'
            ).aggregate(avg=Avg('marks_obtained'))['avg']
        else:
            average_marks = None
        
        return Response({
            'assignment_id': assignment.id,
            'title': assignment.title,
            'total_students': total_students,
            'submitted': submitted_count,
            'not_submitted': total_students - submitted_count,
            'graded': graded_count,
            'pending_grading': pending_count + late_count,
            'late_submissions': late_count,
            'average_marks': average_marks,
            'submission_rate': round((submitted_count / total_students * 100), 2) if total_students > 0 else 0
        })
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """Publish assignment"""
        assignment = self.get_object()
        assignment.is_published = True
        assignment.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='UPDATE',
            model_name='Assignment',
            object_id=str(assignment.id),
            changes={'is_published': True},
            ip_address=request.META.get('REMOTE_ADDR', '')
        )
        
        return Response({'message': 'Assignment published successfully'})
    
    @action(detail=True, methods=['post'])
    def unpublish(self, request, pk=None):
        """Unpublish assignment"""
        assignment = self.get_object()
        assignment.is_published = False
        assignment.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='UPDATE',
            model_name='Assignment',
            object_id=str(assignment.id),
            changes={'is_published': False},
            ip_address=request.META.get('REMOTE_ADDR', '')
        )
        
        return Response({'message': 'Assignment unpublished successfully'})
    
    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """Create assignments for multiple classes/sections"""
        serializer = AssignmentBulkCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        class_ids = data.pop('class_ids')
        section_ids = data.pop('section_ids')
        
        teacher = request.user.teacher_profile
        
        created = []
        errors = []
        
        for class_id in class_ids:
            for section_id in section_ids:
                try:
                    assignment = Assignment.objects.create(
                        teacher=teacher,
                        class_group_id=class_id,
                        section_id=section_id,
                        **data
                    )
                    created.append({
                        'class_id': class_id,
                        'section_id': section_id,
                        'assignment_id': assignment.id
                    })
                except Exception as e:
                    errors.append({
                        'class_id': class_id,
                        'section_id': section_id,
                        'error': str(e)
                    })
        
        AuditLog.objects.create(
            user=request.user,
            action='CREATE',
            model_name='Assignment',
            object_id='bulk',
            changes={'created': len(created), 'errors': len(errors)},
            ip_address=request.META.get('REMOTE_ADDR', '')
        )
        
        return Response({
            'created': created,
            'errors': errors
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming assignments"""
        days = int(request.query_params.get('days', 7))
        end_date = timezone.now() + timedelta(days=days)
        
        assignments = self.get_queryset().filter(
            due_date__lte=end_date,
            due_date__gte=timezone.now(),
            is_published=True
        ).order_by('due_date')
        
        page = self.paginate_queryset(assignments)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(assignments, many=True)
        return Response(serializer.data)

class SubmissionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Submission CRUD operations
    """
    queryset = Submission.objects.all().select_related(
        'assignment', 'student__user', 'graded_by__user'
    ).order_by('-submission_date')
    
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        'assignment': ['exact'],
        'student': ['exact'],
        'status': ['exact'],
        'submission_date': ['gte', 'lte'],
        'graded_at': ['gte', 'lte'],
    }
    search_fields = ['student__user__first_name', 'student__user__last_name', 'comments', 'feedback']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by user role
        user = self.request.user
        if user.has_role('student'):
            student = user.student_profile
            if student:
                queryset = queryset.filter(student=student)
        elif user.has_role('teacher'):
            teacher = user.teacher_profile
            if teacher:
                queryset = queryset.filter(assignment__teacher=teacher)
        elif user.has_role('parent'):
            parent = user.parent_profile
            if parent:
                queryset = queryset.filter(student__in=parent.students.all())
        
        return queryset
    
    def perform_create(self, serializer):
        submission = serializer.save()
        
        AuditLog.objects.create(
            user=self.request.user,
            action='CREATE',
            model_name='Submission',
            object_id=str(submission.id),
            changes=SubmissionSerializer(submission).data,
            ip_address=self.request.META.get('REMOTE_ADDR', '')
        )
    
    @action(detail=True, methods=['post'])
    def grade(self, request, pk=None):
        """Grade a submission"""
        submission = self.get_object()
        
        if submission.status == 'graded':
            return Response(
                {'error': 'Submission already graded'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = SubmissionGradeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        submission.marks_obtained = serializer.validated_data['marks_obtained']
        submission.feedback = serializer.validated_data.get('feedback', '')
        submission.status = 'graded'
        submission.graded_by = request.user.teacher_profile
        submission.graded_at = timezone.now()
        submission.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='UPDATE',
            model_name='Submission',
            object_id=str(submission.id),
            changes={'status': 'graded', 'marks': submission.marks_obtained},
            ip_address=request.META.get('REMOTE_ADDR', '')
        )
        
        return Response(SubmissionSerializer(submission).data)
    
    @action(detail=True, methods=['post'])
    def return_for_revision(self, request, pk=None):
        """Return submission for revision"""
        submission = self.get_object()
        
        submission.status = 'returned'
        submission.feedback = request.data.get('feedback', submission.feedback)
        submission.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='UPDATE',
            model_name='Submission',
            object_id=str(submission.id),
            changes={'status': 'returned'},
            ip_address=request.META.get('REMOTE_ADDR', '')
        )
        
        return Response(SubmissionSerializer(submission).data)
    
    @action(detail=False, methods=['get'])
    def pending_grading(self, request):
        """Get submissions pending grading"""
        teacher = request.user.teacher_profile
        if not teacher:
            return Response(
                {'error': 'Only teachers can access this'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        submissions = self.queryset.filter(
            assignment__teacher=teacher,
            status__in=['submitted', 'late']
        ).order_by('submission_date')
        
        page = self.paginate_queryset(submissions)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(submissions, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_submissions(self, request):
        """Get current user's submissions"""
        user = request.user
        
        if user.has_role('student'):
            student = user.student_profile
            submissions = self.queryset.filter(student=student)
        else:
            return Response(
                {'error': 'Only students can access this'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Group by assignment status
        pending = submissions.filter(
            status__in=['submitted', 'late']
        ).count()
        graded = submissions.filter(status='graded').count()
        returned = submissions.filter(status='returned').count()
        
        serializer = self.get_serializer(submissions.order_by('-submission_date'), many=True)
        
        return Response({
            'total': submissions.count(),
            'pending': pending,
            'graded': graded,
            'returned': returned,
            'submissions': serializer.data
        })