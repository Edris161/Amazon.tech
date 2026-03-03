from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from .models import User, Role, AuditLog
from .serializers import (
    UserSerializer, UserCreateSerializer, UserUpdateSerializer,
    LoginSerializer, TokenResponseSerializer, RoleSerializer,
    AuditLogSerializer, ChangePasswordSerializer
)

class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                if not user.is_active:
                    return Response(
                        {'error': 'Account is disabled'}, 
                        status=status.HTTP_401_UNAUTHORIZED
                    )
                
                refresh = RefreshToken.for_user(user)
                
                # Update last login
                user.last_login = timezone.now()
                user.save(update_fields=['last_login'])
                
                # Create audit log
                AuditLog.objects.create(
                    user=user,
                    action='LOGIN',
                    model_name='User',
                    object_id=str(user.id),
                    ip_address=request.META.get('REMOTE_ADDR', ''),
                    changes={'email': user.email}
                )
                
                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'user': UserSerializer(user).data
                })
            else:
                return Response(
                    {'error': 'Invalid credentials'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except User.DoesNotExist:
            return Response(
                {'error': 'Invalid credentials'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        if request.user.is_authenticated:
            AuditLog.objects.create(
                user=request.user,
                action='LOGOUT',
                model_name='User',
                object_id=str(request.user.id),
                ip_address=request.META.get('REMOTE_ADDR', '')
            )
        return Response({'message': 'Logged out successfully'})
    
    @action(detail=False, methods=['post'])
    def refresh_token(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response(
                {'error': 'Refresh token required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            refresh = RefreshToken(refresh_token)
            return Response({
                'access': str(refresh.access_token),
            })
        except Exception as e:
            return Response(
                {'error': 'Invalid refresh token'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Not authenticated'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Not authenticated'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        if not request.user.check_password(serializer.validated_data['old_password']):
            return Response(
                {'old_password': 'Wrong password'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='UPDATE',
            model_name='User',
            object_id=str(request.user.id),
            changes={'password_changed': True},
            ip_address=request.META.get('REMOTE_ADDR', '')
        )
        
        return Response({'message': 'Password changed successfully'})

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().prefetch_related('roles').order_by('-date_joined')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        user = serializer.save()
        AuditLog.objects.create(
            user=self.request.user,
            action='CREATE',
            model_name='User',
            object_id=str(user.id),
            changes=UserSerializer(user).data,
            ip_address=self.request.META.get('REMOTE_ADDR', '')
        )
    
    def perform_update(self, serializer):
        old_data = UserSerializer(self.get_object()).data
        user = serializer.save()
        AuditLog.objects.create(
            user=self.request.user,
            action='UPDATE',
            model_name='User',
            object_id=str(user.id),
            changes={'old': old_data, 'new': UserSerializer(user).data},
            ip_address=self.request.META.get('REMOTE_ADDR', '')
        )
    
    def perform_destroy(self, instance):
        AuditLog.objects.create(
            user=self.request.user,
            action='DELETE',
            model_name='User',
            object_id=str(instance.id),
            changes={'email': instance.email},
            ip_address=self.request.META.get('REMOTE_ADDR', '')
        )
        instance.delete()
    
    @action(detail=True, methods=['post'])
    def assign_roles(self, request, pk=None):
        user = self.get_object()
        role_ids = request.data.get('role_ids', [])
        
        if not role_ids:
            return Response(
                {'error': 'role_ids required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        roles = Role.objects.filter(id__in=role_ids)
        old_roles = list(user.roles.values_list('id', flat=True))
        user.roles.set(roles)
        
        AuditLog.objects.create(
            user=request.user,
            action='UPDATE',
            model_name='User',
            object_id=str(user.id),
            changes={'old_roles': old_roles, 'new_roles': role_ids},
            ip_address=request.META.get('REMOTE_ADDR', '')
        )
        
        return Response(UserSerializer(user).data)
    
    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        user = self.get_object()
        user.is_active = not user.is_active
        user.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='UPDATE',
            model_name='User',
            object_id=str(user.id),
            changes={'is_active': user.is_active},
            ip_address=request.META.get('REMOTE_ADDR', '')
        )
        
        return Response({'is_active': user.is_active})

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all().order_by('name')
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def perform_create(self, serializer):
        role = serializer.save()
        AuditLog.objects.create(
            user=self.request.user,
            action='CREATE',
            model_name='Role',
            object_id=str(role.id),
            changes=RoleSerializer(role).data,
            ip_address=self.request.META.get('REMOTE_ADDR', '')
        )
    
    def perform_update(self, serializer):
        old_data = RoleSerializer(self.get_object()).data
        role = serializer.save()
        AuditLog.objects.create(
            user=self.request.user,
            action='UPDATE',
            model_name='Role',
            object_id=str(role.id),
            changes={'old': old_data, 'new': RoleSerializer(role).data},
            ip_address=self.request.META.get('REMOTE_ADDR', '')
        )
    
    def perform_destroy(self, instance):
        AuditLog.objects.create(
            user=self.request.user,
            action='DELETE',
            model_name='Role',
            object_id=str(instance.id),
            changes={'name': instance.name},
            ip_address=self.request.META.get('REMOTE_ADDR', '')
        )
        instance.delete()

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all().select_related('user').order_by('-timestamp')
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAdminUser]
    filterset_fields = ['user', 'action', 'model_name']
    search_fields = ['user__email', 'model_name', 'changes']