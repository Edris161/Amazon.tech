from rest_framework import serializers
from .models import Program


class ProgramSerializer(serializers.ModelSerializer):
    syllabus_file = serializers.SerializerMethodField()

    class Meta:
        model = Program
        fields = [
            "id",
            "name",
            "description",
            "curriculum",
            "syllabus_file",
        ]

    def get_syllabus_file(self, obj):
        request = self.context.get("request")
        if obj.syllabus_file and request:
            return request.build_absolute_uri(obj.syllabus_file.url)
        return None