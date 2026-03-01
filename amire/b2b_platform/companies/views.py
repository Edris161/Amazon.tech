from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Company
from .serializers import CompanySerializer, CompanyDetailSerializer


class CompanyListView(generics.ListAPIView):
    queryset = Company.objects.prefetch_related(
    'products',
    'certificates',
    'media',
    'timeline'
).distinct()
    serializer_class = CompanySerializer

    # Enable filtering, search, ordering
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    # Filter fields
    filterset_fields = [
        'business_type',
        'is_verified',
        'established_year',
    ]

    # Search fields
    search_fields = [
    'legal_name',
    'description',
    'main_markets',
    'products__name',   # 🔥 Search inside product name
]
    # Ordering fields
    ordering_fields = [
        'created_at',
        'established_year',
    ]


class CompanyDetailView(generics.RetrieveAPIView):
    queryset = Company.objects.all().prefetch_related(
        'products',
        'certificates',
        'media',
        'timeline'
    )
    serializer_class = CompanyDetailSerializer
    lookup_field = 'slug'