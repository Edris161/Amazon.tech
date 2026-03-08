from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Staff
from .serializers import StaffSerializer


class StaffViewSet(ModelViewSet):
    queryset = Staff.objects.all().order_by("-created_at")
    serializer_class = StaffSerializer

    # Enable filtering, searching, and ordering
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    # Fields that can be searched
    search_fields = [
        "name",
        "position",
        "email",
    ]

    # Fields that can be ordered
    ordering_fields = [
        "name",
        "created_at",
    ]

    # Default ordering
    ordering = ["-created_at"]

    def get_serializer_context(self):
        """
        Pass request context to serializer
        so it can build full image URLs
        """
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context