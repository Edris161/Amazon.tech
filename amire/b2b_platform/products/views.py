from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import Product
from .serializers import ProductSerializer


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all().select_related('company', 'category')
    serializer_class = ProductSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['company__slug', 'category__slug']
    search_fields = ['name']


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all().select_related('company', 'category')
    serializer_class = ProductSerializer
    lookup_field = 'slug'