from django.db import models
from students.models import Student

class TransportRoute(models.Model):
    route_name = models.CharField(max_length=100)
    route_number = models.CharField(max_length=20, unique=True)
    start_point = models.CharField(max_length=255)
    end_point = models.CharField(max_length=255)
    distance = models.DecimalField(max_digits=5, decimal_places=2)  # in km
    total_stops = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['route_number']
    
    def __str__(self):
        return f"{self.route_number} - {self.route_name}"

class TransportStop(models.Model):
    route = models.ForeignKey(TransportRoute, on_delete=models.CASCADE, related_name='stops')
    stop_name = models.CharField(max_length=255)
    stop_order = models.IntegerField()
    pickup_time = models.TimeField()
    drop_time = models.TimeField()
    fare = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    class Meta:
        ordering = ['route', 'stop_order']
        unique_together = ['route', 'stop_order']
    
    def __str__(self):
        return f"{self.route.route_name} - {self.stop_name}"

class Vehicle(models.Model):
    VEHICLE_TYPES = [
        ('bus', 'Bus'),
        ('van', 'Van'),
        ('auto', 'Auto Rickshaw'),
    ]
    
    vehicle_number = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPES)
    capacity = models.IntegerField()
    driver_name = models.CharField(max_length=255)
    driver_phone = models.CharField(max_length=15)
    driver_license = models.CharField(max_length=50)
    conductor_name = models.CharField(max_length=255, blank=True)
    conductor_phone = models.CharField(max_length=15, blank=True)
    route = models.ForeignKey(TransportRoute, on_delete=models.SET_NULL, null=True, related_name='vehicles')
    insurance_expiry = models.DateField()
    fitness_expiry = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.vehicle_number} - {self.driver_name}"

class TransportAssignment(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='transport')
    route = models.ForeignKey(TransportRoute, on_delete=models.CASCADE)
    stop = models.ForeignKey(TransportStop, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True)
    academic_year = models.ForeignKey('academics.AcademicYear', on_delete=models.CASCADE)
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2)
    pickup_point = models.CharField(max_length=255)
    drop_point = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['student', 'academic_year']
    
    def __str__(self):
        return f"{self.student.user.full_name} - {self.route.route_name}"