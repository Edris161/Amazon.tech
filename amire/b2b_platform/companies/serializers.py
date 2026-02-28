from rest_framework import serializers
from .models import Company, CompanyTimeline
from products.models import Product
from certificates.models import Certificate
from gallery.models import Media


# ----------------------------
# Timeline Serializer
# ----------------------------
class CompanyTimelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyTimeline
        fields = ['year', 'event']


# ----------------------------
# Nested Product Serializer
# ----------------------------
class ProductNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'image']


# ----------------------------
# Nested Certificate Serializer
# ----------------------------
class CertificateNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ['id', 'name', 'image', 'pdf_file']


# ----------------------------
# Nested Media Serializer
# ----------------------------
class MediaNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id', 'media_type', 'file']


# ----------------------------
# Company List Serializer (LIGHT)
# ----------------------------
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'id',
            'slug',
            'legal_name',
            'logo',
            'business_type',
            'is_verified',
            'established_year',
            'main_markets',
            'created_at',
        ]


# ----------------------------
# Company Detail Serializer (FULL)
# ----------------------------
class CompanyDetailSerializer(serializers.ModelSerializer):
    timeline = CompanyTimelineSerializer(many=True, read_only=True)
    products = ProductNestedSerializer(many=True, read_only=True)
    certificates = CertificateNestedSerializer(many=True, read_only=True)
    media = MediaNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = '__all__'