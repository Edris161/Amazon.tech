from rest_framework.viewsets import ModelViewSet
from .models import News
from .serializers import NewsSerializer

class NewsViewSet(ModelViewSet):
    queryset = News.objects.all().order_by("-published_at")
    serializer_class = NewsSerializer
    lookup_field = "slug"
    search_fields = ["title"]
    ordering_fields = ["published_at"]
    filterset_fields = ["published_at"]
    search_fields = ["title"]
    ordering_fields = ["published_at"]