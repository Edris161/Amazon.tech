from rest_framework import serializers
from .models import Admission


class AdmissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Admission
        fields = [
            "id",
            "student_name",
            "father_name",
            "email",
            "phone",
            "grade",
            "message",
            "status",
            "created_at",
        ]

        read_only_fields = [
            "status",
            "created_at",
        ]

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email is required.")
        return value