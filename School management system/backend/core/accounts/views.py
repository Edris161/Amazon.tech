from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login, logout
from .models import User, Role, AuditLog
from .serializers import (
    UserSerializer, UserCreateSerializer, LoginSerializer,
    TokenResponseSerializer, RoleSerializer, AuditLogSerializer
)
from .permissions import IsSuperAdmin, IsAdminOrReadOnly
from django.utils import timezone

class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        login(request, user)
        
        refresh = RefreshToken.for_user(user)
        
        # Create audit log
        AuditLog.objects.create(
            user=user,
            action='LOGIN',
            model_name='User',
            object_id=user.id,
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        })
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        if request.user.is_authenticated:
            AuditLog.objects.create(
                user=request.user,
                action='LOGOUT',
                model_name='User',
                object_id=request.user.id,
                ip_address=request.META.get('REMOTE_ADDR')
            )
            logout(request)
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

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().prefetch_related('roles')
    permission_classes = [IsSuperAdmin]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        user = serializer.save()
        AuditLog.objects.create(
            user=self.request.user,
            action='CREATE',
            model_name='User',
            object_id=user.id,
            changes=serializer.data,
            ip_address=self.request.META.get('REMOTE_ADDR')
        )
    
    @action(detail=True, methods=['post'])
    def assign_roles(self, request, pk=None):
        user = self.get_object()
        role_ids = request.data.get('role_ids', [])
        roles = Role.objects.filter(id__in=role_ids)
        user.roles.set(roles)
        
        AuditLog.objects.create(
            user=request.user,
            action='UPDATE',
            model_name='User',
            object_id=user.id,
            changes={'roles': list(role_ids)},
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return Response(UserSerializer(user).data)

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsSuperAdmin]

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all().select_related('user')
    serializer_class = AuditLogSerializer
    permission_classes = [IsSuperAdmin]
    filterset_fields = ['user', 'action', 'model_name']
    search_fields = ['user__email', 'model_name', 'changes']