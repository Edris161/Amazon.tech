# classes/views.py
from rest_framework import viewsets
from .models import ClassRoom, Enrollment
from .serializers import ClassRoomSerializer, EnrollmentSerializer

class ClassRoomViewSet(viewsets.ModelViewSet):
    # Only list active classes by default
    queryset = ClassRoom.objects.filter(is_active=True)
    serializer_class = ClassRoomSerializer
    filterset_fields = ['level', 'teacher_name']

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
