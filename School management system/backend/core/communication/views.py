from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Max
from django.utils import timezone
from .models import Announcement, Message, Notification
from .serializers import (
    AnnouncementSerializer, MessageSerializer, MessageThreadSerializer,
    NotificationSerializer, BulkMessageSerializer
)
from accounts.models import User, Role, AuditLog
from students.models import Student
from teachers.models import Teacher

class AnnouncementViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Announcement CRUD operations
    """
    queryset = Announcement.objects.all().select_related('created_by').prefetch_related(
        'target_roles', 'target_classes', 'target_students', 'target_teachers'
    ).order_by('-created_at')
    
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        'priority': ['exact'],
        'target_all': ['exact'],
        'is_active': ['exact'],
        'publish_from': ['gte', 'lte'],
        'publish_until': ['gte', 'lte'],
        'created_by': ['exact'],
    }
    search_fields = ['title', 'content']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Filter announcements based on user's roles and classes
        if not user.has_role('super_admin') and not user.has_role('school_admin'):
            now = timezone.now()
            queryset = queryset.filter(
                Q(target_all=True) |
                Q(target_roles__in=user.roles.all()) |
                Q(target_students__user=user) |
                Q(target_teachers__user=user)
            ).filter(
                publish_from__lte=now
            ).filter(
                Q(publish_until__isnull=True) | Q(publish_until__gte=now)
            ).distinct()
        
        return queryset
    
    def perform_create(self, serializer):
        announcement = serializer.save()
        
        AuditLog.objects.create(
            user=self.request.user,
            action='CREATE',
            model_name='Announcement',
            object_id=str(announcement.id),
            changes=AnnouncementSerializer(announcement).data,
            ip_address=self.request.META.get('REMOTE_ADDR', '')
        )
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get currently active announcements"""
        now = timezone.now()
        announcements = self.get_queryset().filter(
            is_active=True,
            publish_from__lte=now
        ).filter(
            Q(publish_until__isnull=True) | Q(publish_until__gte=now)
        ).order_by('-priority', '-created_at')
        
        page = self.paginate_queryset(announcements)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(announcements, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pinned(self, request):
        """Get pinned (high priority) announcements"""
        announcements = self.get_queryset().filter(
            priority__in=['high', 'urgent'],
            is_active=True
        ).order_by('-created_at')[:5]
        
        serializer = self.get_serializer(announcements, many=True)
        return Response(serializer.data)

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Message CRUD operations
    """
    queryset = Message.objects.all().select_related(
        'sender', 'recipient', 'parent_message'
    ).order_by('-sent_at')
    
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'sender': ['exact'],
        'recipient': ['exact'],
        'is_read': ['exact'],
        'is_archived': ['exact'],
        'is_starred': ['exact'],
        'sent_at': ['gte', 'lte'],
    }
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Users can only see messages they sent or received
        return queryset.filter(
            Q(sender=user) | Q(recipient=user)
        )
    
    def perform_create(self, serializer):
        message = serializer.save()
        
        # Create notification for recipient
        Notification.objects.create(
            user=message.recipient,
            title=f"New message from {message.sender.full_name}",
            message=message.subject,
            notification_type='info',
            content_type='Message',
            object_id=str(message.id)
        )
        
        AuditLog.objects.create(
            user=self.request.user,
            action='CREATE',
            model_name='Message',
            object_id=str(message.id),
            changes={'subject': message.subject, 'recipient': message.recipient.id},
            ip_address=self.request.META.get('REMOTE_ADDR', '')
        )
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark message as read"""
        message = self.get_object()
        
        if message.recipient != request.user:
            return Response(
                {'error': 'You can only mark your own messages as read'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        message.is_read = True
        message.read_at = timezone.now()
        message.save()
        
        return Response({'message': 'Marked as read'})
    
    @action(detail=True, methods=['post'])
    def toggle_star(self, request, pk=None):
        """Toggle star status of message"""
        message = self.get_object()
        message.is_starred = not message.is_starred
        message.save()
        
        return Response({'is_starred': message.is_starred})
    
    @action(detail=True, methods=['post'])
    def toggle_archive(self, request, pk=None):
        """Toggle archive status of message"""
        message = self.get_object()
        message.is_archived = not message.is_archived
        message.save()
        
        return Response({'is_archived': message.is_archived})
    
    @action(detail=True, methods=['post'])
    def reply(self, request, pk=None):
        """Reply to a message"""
        original = self.get_object()
        
        content = request.data.get('content')
        if not content:
            return Response(
                {'error': 'Content required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        reply = Message.objects.create(
            sender=request.user,
            recipient=original.sender,
            subject=f"Re: {original.subject}",
            content=content,
            parent_message=original
        )
        
        serializer = self.get_serializer(reply)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def inbox(self, request):
        """Get received messages"""
        messages = self.get_queryset().filter(
            recipient=request.user,
            is_archived=False
        ).order_by('-sent_at')
        
        unread_count = messages.filter(is_read=False).count()
        
        page = self.paginate_queryset(messages)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'unread_count': unread_count,
                'messages': serializer.data
            })
        
        serializer = self.get_serializer(messages, many=True)
        return Response({
            'unread_count': unread_count,
            'messages': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def sent(self, request):
        """Get sent messages"""
        messages = self.get_queryset().filter(
            sender=request.user
        ).order_by('-sent_at')
        
        page = self.paginate_queryset(messages)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def threads(self, request):
        """Get message threads"""
        user = request.user
        
        # Get all messages sent or received by user
        messages = Message.objects.filter(
            Q(sender=user) | Q(recipient=user)
        ).order_by('sender', 'recipient', '-sent_at')
        
        # Group by other user
        threads = {}
        for message in messages:
            other_user = message.recipient if message.sender == user else message.sender
            
            if other_user.id not in threads:
                threads[other_user.id] = {
                    'other_user': other_user,
                    'last_message': message,
                    'unread_count': 0,
                    'total_messages': 0
                }
            
            threads[other_user.id]['total_messages'] += 1
            if message.recipient == user and not message.is_read:
                threads[other_user.id]['unread_count'] += 1
        
        # Convert to list and sort by last message time
        thread_list = sorted(
            threads.values(),
            key=lambda x: x['last_message'].sent_at,
            reverse=True
        )
        
        serializer = MessageThreadSerializer(thread_list, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def bulk_send(self, request):
        """Send message to multiple recipients"""
        serializer = BulkMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        recipient_ids = data['recipient_ids']
        
        recipients = User.objects.filter(id__in=recipient_ids)
        sent = []
        failed = []
        
        for recipient in recipients:
            try:
                message = Message.objects.create(
                    sender=request.user,
                    recipient=recipient,
                    subject=data['subject'],
                    content=data['content']
                )
                sent.append({
                    'user_id': recipient.id,
                    'user_name': recipient.full_name,
                    'message_id': message.id
                })
            except Exception as e:
                failed.append({
                    'user_id': recipient.id,
                    'error': str(e)
                })
        
        return Response({
            'sent': sent,
            'failed': failed
        }, status=status.HTTP_201_CREATED)

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing notifications
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'is_read': ['exact'],
        'notification_type': ['exact'],
        'created_at': ['gte', 'lte'],
    }
    
    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user
        ).order_by('-created_at')
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark notification as read"""
        notification = self.get_object()
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save()
        
        return Response({'message': 'Marked as read'})
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all notifications as read"""
        self.get_queryset().filter(is_read=False).update(
            is_read=True,
            read_at=timezone.now()
        )
        
        return Response({'message': 'All notifications marked as read'})
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get count of unread notifications"""
        count = self.get_queryset().filter(is_read=False).count()
        return Response({'unread_count': count})
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent notifications"""
        notifications = self.get_queryset()[:10]
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)