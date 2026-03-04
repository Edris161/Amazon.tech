from rest_framework import serializers
from .models import Teacher


class TeacherSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = [
            "id",
            "full_name",
            "subject",
            "bio",
            "photo",
            "email",
            "phone",
        ]

    def get_photo(self, obj):
        request = self.context.get("request")
        if obj.photo and request:
            return request.build_absolute_uri(obj.photo.url)
        return None

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"