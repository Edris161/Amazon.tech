from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from .models import News
from .serializers import NewsListSerializer, NewsDetailSerializer


class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /api/news/
    GET /api/news/{slug}/
    """

    permission_classes = [AllowAny]
    lookup_field = "slug"
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title"]
    ordering_fields = ["published_at"]
    ordering = ["-published_at"]

    def get_queryset(self):
        return News.objects.filter(
            is_published=True,
            published_at__lte=timezone.now()
        )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return NewsDetailSerializer
        return NewsListSerializer