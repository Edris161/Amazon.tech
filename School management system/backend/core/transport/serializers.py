from rest_framework import serializers
from students.serializers import StudentSerializer
from academics.serializers import AcademicYearSerializer
from .models import TransportRoute, TransportStop, Vehicle, TransportAssignment
from django.utils import timezone

class TransportRouteSerializer(serializers.ModelSerializer):
    stops_count = serializers.IntegerField(source='stops.count', read_only=True)
    vehicles_count = serializers.IntegerField(source='vehicles.count', read_only=True)
    students_count = serializers.SerializerMethodField()
    
    class Meta:
        model = TransportRoute
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
    
    def get_students_count(self, obj):
        return obj.transport_assignments.filter(is_active=True).count()

class TransportStopSerializer(serializers.ModelSerializer):
    route_name = serializers.CharField(source='route.route_name', read_only=True)
    route_number = serializers.CharField(source='route.route_number', read_only=True)
    
    class Meta:
        model = TransportStop
        fields = '__all__'
        read_only_fields = ['id']
    
    def validate(self, data):
        # Check if stop order already exists for this route
        if TransportStop.objects.filter(
            route=data['route'],
            stop_order=data['stop_order']
        ).exists() and not self.instance:
            raise serializers.ValidationError(
                f"Stop order {data['stop_order']} already exists for this route"
            )
        return data

class VehicleSerializer(serializers.ModelSerializer):
    route_name = serializers.CharField(source='route.route_name', read_only=True, allow_null=True)
    route_number = serializers.CharField(source='route.route_number', read_only=True, allow_null=True)
    students_assigned = serializers.SerializerMethodField()
    is_insurance_valid = serializers.SerializerMethodField()
    is_fitness_valid = serializers.SerializerMethodField()
    
    class Meta:
        model = Vehicle
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
    
    def get_students_assigned(self, obj):
        return obj.transport_assignments.filter(is_active=True).count()
    
    def get_is_insurance_valid(self, obj):
        return obj.insurance_expiry >= timezone.now().date()
    
    def get_is_fitness_valid(self, obj):
        return obj.fitness_expiry >= timezone.now().date()
    
    def validate(self, data):
        if data.get('insurance_expiry') and data['insurance_expiry'] < timezone.now().date():
            raise serializers.ValidationError("Insurance expiry cannot be in the past")
        
        if data.get('fitness_expiry') and data['fitness_expiry'] < timezone.now().date():
            raise serializers.ValidationError("Fitness expiry cannot be in the past")
        
        return data

class TransportAssignmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.full_name', read_only=True)
    student_roll = serializers.CharField(source='student.roll_number', read_only=True)
    student_class = serializers.CharField(source='student.current_class.name', read_only=True)
    student_section = serializers.CharField(source='student.current_section.name', read_only=True)
    route_name = serializers.CharField(source='route.route_name', read_only=True)
    route_number = serializers.CharField(source='route.route_number', read_only=True)
    stop_name = serializers.CharField(source='stop.stop_name', read_only=True)
    stop_order = serializers.IntegerField(source='stop.stop_order', read_only=True)
    vehicle_number = serializers.CharField(source='vehicle.vehicle_number', read_only=True, allow_null=True)
    academic_year_name = serializers.CharField(source='academic_year.name', read_only=True)
    
    class Meta:
        model = TransportAssignment
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, data):
        # Check if student already has transport assignment for this academic year
        if TransportAssignment.objects.filter(
            student=data['student'],
            academic_year=data['academic_year'],
            is_active=True
        ).exists() and not self.instance:
            raise serializers.ValidationError(
                "Student already has transport assignment for this academic year"
            )
        
        # Check if vehicle has capacity
        if data.get('vehicle'):
            current_assignments = TransportAssignment.objects.filter(
                vehicle=data['vehicle'],
                is_active=True
            ).count()
            
            if current_assignments >= data['vehicle'].capacity:
                raise serializers.ValidationError(
                    f"Vehicle has reached maximum capacity of {data['vehicle'].capacity}"
                )
        
        return data

class TransportBulkAssignSerializer(serializers.Serializer):
    student_ids = serializers.ListField(child=serializers.IntegerField())
    route_id = serializers.IntegerField()
    stop_id = serializers.IntegerField()
    vehicle_id = serializers.IntegerField(required=False, allow_null=True)
    academic_year_id = serializers.IntegerField()
    monthly_fee = serializers.DecimalField(max_digits=10, decimal_places=2)

class RouteReportSerializer(serializers.Serializer):
    route_id = serializers.IntegerField()
    route_name = serializers.CharField()
    total_students = serializers.IntegerField()
    total_stops = serializers.IntegerField()
    vehicles = serializers.ListField(child=serializers.DictField())
    stops = serializers.ListField(child=serializers.DictField())
    monthly_revenue = serializers.DecimalField(max_digits=15, decimal_places=2)