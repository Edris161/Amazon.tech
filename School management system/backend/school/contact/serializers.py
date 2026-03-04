from rest_framework import serializers
from .models import ContactMessage


class ContactMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactMessage
        fields = [
            "id",
            "name",
            "email",
            "message",
            "submitted_at",
        ]
        read_only_fields = ["id", "submitted_at"]

    def validate_message(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Message is too short.")
        return value