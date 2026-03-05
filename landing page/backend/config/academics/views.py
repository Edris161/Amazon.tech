from rest_framework.viewsets import ModelViewSet
from .models import Academics
from .serializers import AcademicsSerializer

class AcademicsViewSet(ModelViewSet):
    queryset = Academics.objects.all().order_by("-created_at")
    serializer_class = AcademicsSerializer