from rest_framework import serializers
from .models import Academics


class AcademicsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Academics
        fields = [
            "id",
            "title",
            "description",
            "grade_level",
            "subjects",
            "duration",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
        ]