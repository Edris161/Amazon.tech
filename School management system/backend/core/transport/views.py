from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Sum
from django.utils import timezone
from datetime import timedelta
from .models import TransportRoute, TransportStop, Vehicle, TransportAssignment
from .serializers import (
    TransportRouteSerializer, TransportStopSerializer,
    VehicleSerializer, TransportAssignmentSerializer,
    TransportBulkAssignSerializer, RouteReportSerializer
)
from students.models import Student
from accounts.models import AuditLog

class TransportRouteViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Transport Route CRUD operations
    """
    queryset = TransportRoute.objects.all().prefetch_related(
        'stops', 'vehicles'
    ).order_by('route_number')
    
    serializer_class = TransportRouteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['route_name', 'route_number', 'start_point', 'end_point']
    
    def perform_create(self, serializer):
        route = serializer.save()
        
        AuditLog.objects.create(
            user=self.request.user,
            action='CREATE',
            model_name='TransportRoute',
            object_id=str(route.id),
            changes=TransportRouteSerializer(route).data,
            ip_address=self.request.META.get('REMOTE_ADDR', '')
        )
    
    @action(detail=True, methods=['get'])
    def stops(self, request, pk=None):
        """Get all stops on this route"""
        route = self.get_object()
        stops = route.stops.all().order_by('stop_order')
        serializer = TransportStopSerializer(stops, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def vehicles(self, request, pk=None):
        """Get all vehicles assigned to this route"""
        route = self.get_object()
        vehicles = route.vehicles.filter(is_active=True)
        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        """Get all students on this route"""
        route = self.get_object()
        assignments = route.transport_assignments.filter(
            is_active=True
        ).select_related('student__user', 'stop')
        
        data = []
        for assignment in assignments:
            data.append({
                'student_id': assignment.student.id,
                'student_name': assignment.student.user.full_name,
                'roll_number': assignment.student.roll_number,
                'class': assignment.student.current_class.name,
                'section': assignment.student.current_section.name,
                'stop': assignment.stop.stop_name,
                'pickup_time': assignment.stop.pickup_time,
                'drop_time': assignment.stop.drop_time,
                'vehicle': assignment.vehicle.vehicle_number if assignment.vehicle else None
            })
        
        return Response(data)
    
    @action(detail=True, methods=['get'])
    def report(self, request, pk=None):
        """Get detailed route report"""
        route = self.get_object()
        
        assignments = route.transport_assignments.filter(is_active=True)
        total_students = assignments.count()
        monthly_revenue = assignments.aggregate(total=Sum('monthly_fee'))['total'] or 0
        
        vehicles = []
        for vehicle in route.vehicles.filter(is_active=True):
            vehicles.append({
                'id': vehicle.id,
                'vehicle_number': vehicle.vehicle_number,
                'driver_name': vehicle.driver_name,
                'capacity': vehicle.capacity,
                'students_assigned': vehicle.transport_assignments.filter(is_active=True).count()
            })
        
        stops = []
        for stop in route.stops.all().order_by('stop_order'):
            stops.append({
                'id': stop.id,
                'stop_name': stop.stop_name,
                'pickup_time': stop.pickup_time,
                'drop_time': stop.drop_time,
                'students': stop.transport_assignments.filter(is_active=True).count()
            })
        
        serializer = RouteReportSerializer(data={
            'route_id': route.id,
            'route_name': route.route_name,
            'total_students': total_students,
            'total_stops': route.stops.count(),
            'vehicles': vehicles,
            'stops': stops,
            'monthly_revenue': monthly_revenue
        })
        serializer.is_valid()
        
        return Response(serializer.data)

class TransportStopViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Transport Stop CRUD operations
    """
    queryset = TransportStop.objects.all().select_related('route').order_by('route', 'stop_order')
    serializer_class = TransportStopSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['route']
    
    def perform_create(self, serializer):
        stop = serializer.save()
        
        AuditLog.objects.create(
            user=self.request.user,
            action='CREATE',
            model_name='TransportStop',
            object_id=str(stop.id),
            changes=TransportStopSerializer(stop).data,
            ip_address=self.request.META.get('REMOTE_ADDR', '')
        )
    
    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        """Get students assigned to this stop"""
        stop = self.get_object()
        assignments = stop.transport_assignments.filter(
            is_active=True
        ).select_related('student__user')
        
        data = []
        for assignment in assignments:
            data.append({
                'student_id': assignment.student.id,
                'student_name': assignment.student.user.full_name,
                'roll_number': assignment.student.roll_number,
                'class': assignment.student.current_class.name,
                'section': assignment.student.current_section.name,
                'vehicle': assignment.vehicle.vehicle_number if assignment.vehicle else None
            })
        
        return Response(data)

class VehicleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Vehicle CRUD operations
    """
    queryset = Vehicle.objects.all().select_related('route').order_by('vehicle_number')
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        'route': ['exact', 'isnull'],
        'vehicle_type': ['exact'],
        'is_active': ['exact'],
        'insurance_expiry': ['gte', 'lte'],
        'fitness_expiry': ['gte', 'lte'],
    }
    search_fields = ['vehicle_number', 'driver_name', 'driver_phone']
    
    def perform_create(self, serializer):
        vehicle = serializer.save()
        
        AuditLog.objects.create(
            user=self.request.user,
            action='CREATE',
            model_name='Vehicle',
            object_id=str(vehicle.id),
            changes=VehicleSerializer(vehicle).data,
            ip_address=self.request.META.get('REMOTE_ADDR', '')
        )
    
    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        """Get students assigned to this vehicle"""
        vehicle = self.get_object()
        assignments = vehicle.transport_assignments.filter(
            is_active=True
        ).select_related('student__user', 'stop')
        
        data = []
        for assignment in assignments:
            data.append({
                'student_id': assignment.student.id,
                'student_name': assignment.student.user.full_name,
                'roll_number': assignment.student.roll_number,
                'class': assignment.student.current_class.name,
                'section': assignment.student.current_section.name,
                'stop': assignment.stop.stop_name,
                'pickup_time': assignment.stop.pickup_time,
                'drop_time': assignment.stop.drop_time
            })
        
        return Response(data)
    
    @action(detail=False, methods=['get'])
    def expiring_soon(self, request):
        """Get vehicles with expiring insurance/fitness"""
        days = int(request.query_params.get('days', 30))
        expiry_date = timezone.now().date() + timedelta(days=days)
        
        vehicles = self.queryset.filter(
            Q(insurance_expiry__lte=expiry_date) |
            Q(fitness_expiry__lte=expiry_date)
        )
        
        serializer = self.get_serializer(vehicles, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def update_driver(self, request, pk=None):
        """Update vehicle driver details"""
        vehicle = self.get_object()
        
        vehicle.driver_name = request.data.get('driver_name', vehicle.driver_name)
        vehicle.driver_phone = request.data.get('driver_phone', vehicle.driver_phone)
        vehicle.driver_license = request.data.get('driver_license', vehicle.driver_license)
        vehicle.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='UPDATE',
            model_name='Vehicle',
            object_id=str(vehicle.id),
            changes={'driver_updated': True},
            ip_address=self.request.META.get('REMOTE_ADDR', '')
        )
        
        return Response(VehicleSerializer(vehicle).data)

class TransportAssignmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Transport Assignment CRUD operations
    """
    queryset = TransportAssignment.objects.all().select_related(
        'student__user', 'route', 'stop', 'vehicle', 'academic_year'
    ).order_by('-created_at')
    
    serializer_class = TransportAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'student': ['exact'],
        'route': ['exact'],
        'stop': ['exact'],
        'vehicle': ['exact', 'isnull'],
        'academic_year': ['exact'],
        'is_active': ['exact'],
    }
    
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
        assignment = serializer.save()
        
        AuditLog.objects.create(
            user=self.request.user,
            action='CREATE',
            model_name='TransportAssignment',
            object_id=str(assignment.id),
            changes=TransportAssignmentSerializer(assignment).data,
            ip_address=self.request.META.get('REMOTE_ADDR', '')
        )
    
    @action(detail=False, methods=['post'])
    def bulk_assign(self, request):
        """Assign transport to multiple students"""
        serializer = TransportBulkAssignSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        student_ids = data['student_ids']
        
        created = []
        errors = []
        
        for student_id in student_ids:
            try:
                student = Student.objects.get(id=student_id)
                
                # Check if already assigned
                existing = TransportAssignment.objects.filter(
                    student=student,
                    academic_year_id=data['academic_year_id'],
                    is_active=True
                ).first()
                
                if existing:
                    # Update existing
                    existing.route_id = data['route_id']
                    existing.stop_id = data['stop_id']
                    existing.vehicle_id = data.get('vehicle_id')
                    existing.monthly_fee = data['monthly_fee']
                    existing.save()
                    created.append({'student_id': student_id, 'status': 'updated'})
                else:
                    # Create new
                    assignment = TransportAssignment.objects.create(
                        student=student,
                        route_id=data['route_id'],
                        stop_id=data['stop_id'],
                        vehicle_id=data.get('vehicle_id'),
                        academic_year_id=data['academic_year_id'],
                        monthly_fee=data['monthly_fee'],
                        pickup_point=student.address_line1,
                        drop_point=student.address_line1
                    )
                    created.append({'student_id': student_id, 'status': 'created'})
                    
            except Student.DoesNotExist:
                errors.append({'student_id': student_id, 'error': 'Student not found'})
            except Exception as e:
                errors.append({'student_id': student_id, 'error': str(e)})
        
        AuditLog.objects.create(
            user=request.user,
            action='CREATE',
            model_name='TransportAssignment',
            object_id='bulk',
            changes={'created': len(created), 'errors': len(errors)},
            ip_address=request.META.get('REMOTE_ADDR', '')
        )
        
        return Response({
            'created': created,
            'errors': errors
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate transport assignment"""
        assignment = self.get_object()
        assignment.is_active = False
        assignment.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='UPDATE',
            model_name='TransportAssignment',
            object_id=str(assignment.id),
            changes={'is_active': False},
            ip_address=request.META.get('REMOTE_ADDR', '')
        )
        
        return Response({'message': 'Transport assignment deactivated'})