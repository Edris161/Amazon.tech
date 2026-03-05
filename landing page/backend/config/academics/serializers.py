from rest_framework import serializers
from .models import Academics

class AcademicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Academics
        fields = "__all__"