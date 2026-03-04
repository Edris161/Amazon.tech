from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Program
from .serializers import ProgramSerializer


class ProgramViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /api/academics/
    GET /api/academics/{id}/
    """

    permission_classes = [AllowAny]
    serializer_class = ProgramSerializer
    queryset = Program.objects.all()