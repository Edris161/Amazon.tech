from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Admission
from .serializers import AdmissionSerializer


class AdmissionViewSet(ModelViewSet):
    queryset = Admission.objects.all().order_by("-created_at")
    serializer_class = AdmissionSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    search_fields = [
        "student_name",
        "father_name",
        "email",
    ]

    filterset_fields = [
        "grade",
        "status",
    ]

    ordering_fields = [
        "created_at",
        "student_name",
    ]

    ordering = [
        "-created_at"
    ]