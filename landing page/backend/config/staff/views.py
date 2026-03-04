from rest_framework.viewsets import ModelViewSet
from .models import Staff
from .serializers import StaffSerializer

class StaffViewSet(ModelViewSet):
    queryset = Staff.objects.all().order_by("-created_at")
    serializer_class = StaffSerializer