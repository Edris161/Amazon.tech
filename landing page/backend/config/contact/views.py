from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Contact
from .serializers import ContactSerializer


class ContactViewSet(ModelViewSet):
    queryset = Contact.objects.all().order_by("-created_at")
    serializer_class = ContactSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    search_fields = [
        "name",
        "email",
        "subject",
    ]

    ordering_fields = [
        "created_at",
        "name",
    ]

    ordering = [
        "-created_at"
    ]