from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Teacher
from .serializers import TeacherSerializer


class TeacherViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /api/staff/
    GET /api/staff/{id}/
    """

    permission_classes = [AllowAny]
    serializer_class = TeacherSerializer

    def get_queryset(self):
        return Teacher.objects.filter(is_active=True)