from rest_framework import serializers
from .models import AdmissionApplication


class AdmissionApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdmissionApplication
        fields = [
            "id",
            "full_name",
            "email",
            "phone",
            "grade_applying",
            "message",
            "submitted_at",
        ]
        read_only_fields = ["id", "submitted_at"]

    def validate_phone(self, value):
        if len(value) < 7:
            raise serializers.ValidationError("Phone number is too short.")
        return value