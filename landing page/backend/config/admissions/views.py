from rest_framework.viewsets import ModelViewSet
from .models import Admission
from .serializers import AdmissionSerializer

class AdmissionViewSet(ModelViewSet):
    queryset = Admission.objects.all().order_by("-created_at")
    serializer_class = AdmissionSerializer