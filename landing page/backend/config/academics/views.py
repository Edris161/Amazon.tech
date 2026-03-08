from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Academics
from .serializers import AcademicsSerializer


class AcademicsViewSet(ModelViewSet):
    queryset = Academics.objects.all().order_by("-created_at")
    serializer_class = AcademicsSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    search_fields = [
        "title",
        "grade_level",
    ]

    ordering_fields = [
        "created_at",
        "title",
    ]

    filterset_fields = [
        "grade_level",
    ]

    ordering = [
        "-created_at"
    ]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context