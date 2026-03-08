from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Gallery
from .serializers import GallerySerializer


class GalleryViewSet(ModelViewSet):
    queryset = Gallery.objects.all().order_by("-uploaded_at")
    serializer_class = GallerySerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "category",
    ]

    search_fields = [
        "title",
        "category",
    ]

    ordering_fields = [
        "uploaded_at",
        "title",
    ]

    ordering = [
        "-uploaded_at"
    ]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context