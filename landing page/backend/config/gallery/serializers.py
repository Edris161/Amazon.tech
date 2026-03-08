from rest_framework import serializers
from .models import Gallery


class GallerySerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Gallery
        fields = [
            "id",
            "title",
            "category",
            "image",
            "image_url",
            "uploaded_at",
        ]
        read_only_fields = ["uploaded_at"]

    def get_image_url(self, obj):
        request = self.context.get("request")

        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)

        return None