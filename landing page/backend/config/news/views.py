from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import News
from .serializers import NewsSerializer


class NewsViewSet(ModelViewSet):
    queryset = News.objects.all().order_by("-published_at")
    serializer_class = NewsSerializer

    lookup_field = "slug"

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    search_fields = [
        "title",
    ]

    ordering_fields = [
        "published_at",
    ]

    filterset_fields = [
        "published_at",
    ]

    ordering = [
        "-published_at"
    ]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context