from rest_framework import serializers
from .models import Staff


class StaffSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Staff
        fields = [
            "id",
            "name",
            "position",
            "bio",
            "email",
            "phone",
            "photo",
            "photo_url",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def get_photo_url(self, obj):
        request = self.context.get("request")
        if obj.photo and request:
            return request.build_absolute_uri(obj.photo.url)
        return None