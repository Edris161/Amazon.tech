from rest_framework import serializers
from .models import Contact


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = [
            "id",
            "name",
            "email",
            "subject",
            "message",
            "created_at",
        ]

        read_only_fields = [
            "created_at",
        ]

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email is required.")
        return value