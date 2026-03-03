from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Sum
from django.utils import timezone
from datetime import timedelta
from .models import Book, BookIssue, BookReservation
from .serializers import (
    BookSerializer, BookIssueSerializer, BookReservationSerializer,
    BookReturnSerializer, BookSearchSerializer, LibraryStatisticsSerializer
)
from students.models import Student
from teachers.models import Teacher
from accounts.models import AuditLog

class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Book CRUD operations
    """
    queryset = Book.objects.all().order_by('title')
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'category': ['exact'],
        'author': ['exact', 'icontains'],
        'publisher': ['exact', 'icontains'],
        'language': ['exact'],
        'is_active': ['exact'],
        'publication_year': ['exact', 'gte', 'lte'],
    }
    search_fields = ['title', 'author', 'publisher', 'isbn', 'description']
    ordering_fields = ['title', 'author', 'publication_year', 'total_copies']
    
    def perform_create(self, serializer):
        book = serializer.save()
        
        AuditLog.objects.create(
            user=self.request.user,
            action='CREATE',
            model_name='Book',
            object_id=str(book.id),
            changes=BookSerializer(book).data,
            ip_address=self.request.META.get('REMOTE_ADDR', '')
        )
    
    def perform_update(self, serializer):
        old_data = BookSerializer(self.get_object()).data
        book = serializer.save()
        
        AuditLog.objects.create(
            user=self.request.user,
            action='UPDATE',
            model_name='Book',
            object_id=str(book.id),
            changes={'old': old_data, 'new': BookSerializer(book).data},
            ip_address=self.request.META.get('REMOTE_ADDR', '')
        )
    
    @action(detail=True, methods=['get'])
    def issues(self, request, pk=None):
        """Get issue history for this book"""
        book = self.get_object()
        issues = book.issues.all().select_related(
            'student__user', 'teacher__user', 'issued_by'
        ).order_by('-issue_date')
        
        serializer = BookIssueSerializer(issues, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def reservations(self, request, pk=None):
        """Get reservations for this book"""
        book = self.get_object()
        reservations = book.reservations.filter(
            status='pending'
        ).select_related('student__user', 'teacher__user').order_by('reservation_date')
        
        serializer = BookReservationSerializer(reservations, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_copies(self, request, pk=None):
        """Add more copies of this book"""
        book = self.get_object()
        copies_to_add = request.data.get('copies', 1)
        
        book.total_copies += copies_to_add
        book.available_copies += copies_to_add
        book.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='UPDATE',
            model_name='Book',
            object_id=str(book.id),
            changes={'added_copies': copies_to_add},
            ip_address=self.request.META.get('REMOTE_ADDR', '')
        )
        
        return Response(BookSerializer(book).data)
    
    @action(detail=True, methods=['post'])
    def remove_copies(self, request, pk=None):
        """Remove copies of this book"""
        book = self.get_object()
        copies_to_remove = request.data.get('copies', 1)
        
        if copies_to_remove > book.available_copies:
            return Response(
                {'error': f'Cannot remove {copies_to_remove} copies. Only {book.available_copies} are available'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        book.total_copies -= copies_to_remove
        book.available_copies -= copies_to_remove
        book.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='UPDATE',
            model_name='Book',
            object_id=str(book.id),
            changes={'removed_copies': copies_to_remove},
            ip_address=request.META.get('REMOTE_ADDR', '')
        )
        
        return Response(BookSerializer(book).data)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Advanced book search"""
        serializer = BookSearchSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        queryset = self.get_queryset()
        
        if data.get('query'):
            queryset = queryset.filter(
                Q(title__icontains=data['query']) |
                Q(author__icontains=data['query']) |
                Q(isbn__icontains=data['query'])
            )
        
        if data.get('category'):
            queryset = queryset.filter(category=data['category'])
        
        if data.get('author'):
            queryset = queryset.filter(author__icontains=data['author'])
        
        if data.get('publisher'):
            queryset = queryset.filter(publisher__icontains=data['publisher'])
        
        if data.get('language'):
            queryset = queryset.filter(language=data['language'])
        
        if data.get('available_only'):
            queryset = queryset.filter(available_copies__gt=0)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get library statistics"""
        total_books = Book.objects.count()
        total_copies = Book.objects.aggregate(total=Sum('total_copies'))['total'] or 0
        available_copies = Book.objects.aggregate(total=Sum('available_copies'))['total'] or 0
        issued_books = BookIssue.objects.filter(status='issued').count()
        overdue_books = BookIssue.objects.filter(
            status='issued',
            due_date__lt=timezone.now().date()
        ).count()
        pending_reservations = BookReservation.objects.filter(status='pending').count()
        
        # Category breakdown
        category_breakdown = Book.objects.values('category').annotate(
            count=Count('id'),
            total_copies=Sum('total_copies'),
            available_copies=Sum('available_copies')
        ).order_by('category')
        
        # Most borrowed books
        most_borrowed = Book.objects.annotate(
            issue_count=Count('issues')
        ).order_by('-issue_count')[:10]
        
        serializer = LibraryStatisticsSerializer(data={
            'total_books': total_books,
            'total_copies': total_copies,
            'available_copies': available_copies,
            'issued_books': issued_books,
            'overdue_books': overdue_books,
            'pending_reservations': pending_reservations,
            'category_breakdown': list(category_breakdown),
            'most_borrowed': BookSerializer(most_borrowed, many=True).data
        })
        serializer.is_valid()
        
        return Response(serializer.data)

class BookIssueViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Book Issue CRUD operations
    """
    queryset = BookIssue.objects.all().select_related(
        'book', 'student__user', 'teacher__user', 'issued_by'
    ).order_by('-issue_date')
    
    serializer_class = BookIssueSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        'book': ['exact'],
        'student': ['exact'],
        'teacher': ['exact'],
        'status': ['exact'],
        'issue_date': ['gte', 'lte'],
        'due_date': ['gte', 'lte'],
        'return_date': ['gte', 'lte'],
    }
    search_fields = ['book__title', 'book__author', 'remarks']
    
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
                queryset = queryset.filter(teacher=teacher)
        elif user.has_role('parent'):
            parent = user.parent_profile
            if parent:
                queryset = queryset.filter(student__in=parent.students.all())
        
        return queryset
    
    def perform_create(self, serializer):
        issue = serializer.save()
        
        AuditLog.objects.create(
            user=self.request.user,
            action='CREATE',
            model_name='BookIssue',
            object_id=str(issue.id),
            changes=BookIssueSerializer(issue).data,
            ip_address=self.request.META.get('REMOTE_ADDR', '')
        )
    
    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        """Return an issued book"""
        issue = self.get_object()
        
        if issue.status != 'issued':
            return Response(
                {'error': f'Book is already {issue.status}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = BookReturnSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        issue.return_date = data['return_date']
        issue.status = 'returned'
        
        # Calculate fine if overdue
        if issue.due_date < data['return_date']:
            days_overdue = (data['return_date'] - issue.due_date).days
            issue.fine_amount = days_overdue * 10  # ₹10 per day
        
        if data['condition'] == 'damaged':
            issue.status = 'damaged'
            issue.fine_amount += issue.book.price * 0.5  # 50% of book price
        elif data['condition'] == 'lost':
            issue.status = 'lost'
            issue.fine_amount += issue.book.price  # Full book price
        
        if data['fine_paid']:
            issue.fine_paid = True
        
        issue.remarks = data.get('remarks', '')
        issue.save()
        
        # Increase available copies if not lost or damaged
        if issue.status == 'returned':
            issue.book.available_copies += 1
            issue.book.save()
        
        # Check for pending reservations
        if issue.status == 'returned':
            pending_reservation = BookReservation.objects.filter(
                book=issue.book,
                status='pending'
            ).order_by('reservation_date').first()
            
            if pending_reservation:
                pending_reservation.status = 'available'
                pending_reservation.notified = False
                pending_reservation.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='UPDATE',
            model_name='BookIssue',
            object_id=str(issue.id),
            changes={'status': issue.status, 'return_date': issue.return_date},
            ip_address=request.META.get('REMOTE_ADDR', '')
        )
        
        return Response(BookIssueSerializer(issue).data)
    
    @action(detail=True, methods=['post'])
    def renew(self, request, pk=None):
        """Renew an issued book"""
        issue = self.get_object()
        
        if issue.status != 'issued':
            return Response(
                {'error': f'Cannot renew book with status {issue.status}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Extend due date by 7 days
        issue.due_date = issue.due_date + timedelta(days=7)
        issue.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='UPDATE',
            model_name='BookIssue',
            object_id=str(issue.id),
            changes={'due_date': issue.due_date, 'renewed': True},
            ip_address=request.META.get('REMOTE_ADDR', '')
        )
        
        return Response(BookIssueSerializer(issue).data)
    
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Get all overdue books"""
        overdue_books = self.queryset.filter(
            status='issued',
            due_date__lt=timezone.now().date()
        ).order_by('due_date')
        
        # Calculate fines
        for book in overdue_books:
            book.calculate_fine()
        
        page = self.paginate_queryset(overdue_books)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(overdue_books, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_books(self, request):
        """Get books issued to current user"""
        user = request.user
        
        if user.has_role('student'):
            student = user.student_profile
            issues = self.queryset.filter(student=student)
        elif user.has_role('teacher'):
            teacher = user.teacher_profile
            issues = self.queryset.filter(teacher=teacher)
        else:
            return Response(
                {'error': 'Only students and teachers can access this'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        current_issues = issues.filter(status='issued')
        past_issues = issues.filter(status__in=['returned', 'lost', 'damaged'])
        
        return Response({
            'current_issues': BookIssueSerializer(current_issues, many=True).data,
            'past_issues': BookIssueSerializer(past_issues, many=True).data,
            'total_current': current_issues.count(),
            'total_overdue': current_issues.filter(due_date__lt=timezone.now().date()).count()
        })

class BookReservationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Book Reservation CRUD operations
    """
    queryset = BookReservation.objects.all().select_related(
        'book', 'student__user', 'teacher__user'
    ).order_by('reservation_date')
    
    serializer_class = BookReservationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'book': ['exact'],
        'student': ['exact'],
        'teacher': ['exact'],
        'status': ['exact'],
        'reservation_date': ['gte', 'lte'],
    }
    
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
                queryset = queryset.filter(teacher=teacher)
        
        return queryset
    
    def perform_create(self, serializer):
        reservation = serializer.save()
        
        AuditLog.objects.create(
            user=self.request.user,
            action='CREATE',
            model_name='BookReservation',
            object_id=str(reservation.id),
            changes=BookReservationSerializer(reservation).data,
            ip_address=self.request.META.get('REMOTE_ADDR', '')
        )
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a reservation"""
        reservation = self.get_object()
        
        if reservation.status != 'pending':
            return Response(
                {'error': f'Cannot cancel reservation with status {reservation.status}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        reservation.status = 'cancelled'
        reservation.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='UPDATE',
            model_name='BookReservation',
            object_id=str(reservation.id),
            changes={'status': 'cancelled'},
            ip_address=request.META.get('REMOTE_ADDR', '')
        )
        
        return Response(BookReservationSerializer(reservation).data)
    
    @action(detail=True, methods=['post'])
    def notify_available(self, request, pk=None):
        """Notify that reserved book is available"""
        reservation = self.get_object()
        
        if reservation.status != 'available':
            return Response(
                {'error': f'Book is not available for reservation'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        reservation.notified = True
        reservation.save()
        
        # Here you would send actual notification (email/SMS)
        
        return Response({'message': 'Notification sent successfully'})
    
    @action(detail=False, methods=['get'])
    def my_reservations(self, request):
        """Get current user's reservations"""
        user = request.user
        
        if user.has_role('student'):
            student = user.student_profile
            reservations = self.queryset.filter(student=student)
        elif user.has_role('teacher'):
            teacher = user.teacher_profile
            reservations = self.queryset.filter(teacher=teacher)
        else:
            return Response(
                {'error': 'Only students and teachers can access this'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        pending = reservations.filter(status='pending')
        available = reservations.filter(status='available')
        
        return Response({
            'pending': BookReservationSerializer(pending, many=True).data,
            'available': BookReservationSerializer(available, many=True).data
        }) 
   