from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from .models import GalleryImage
from .serializers import GalleryImageSerializer


class GalleryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /api/gallery/
    Optional filter:
    /api/gallery/?event_name=Sports
    """

    permission_classes = [AllowAny]
    serializer_class = GalleryImageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["event_name"]
    queryset = GalleryImage.objects.all()