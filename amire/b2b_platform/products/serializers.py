from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.legal_name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'image',
            'company',
            'company_name',
            'category',
            'category_name',
            'created_at',
        ]