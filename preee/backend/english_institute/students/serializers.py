"""
Students serializers module.
Handles serialization of Student and Level data.
"""

from rest_framework import serializers
from .models import Student, Level

class LevelSerializer(serializers.ModelSerializer):
    """
    Serializer for Level model.
    """
    
    class Meta:
        model = Level
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    """
    Serializer for Student model.
    Includes level details in responses.
    """
    
    level_name = serializers.CharField(source='level.name', read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = '__all__'
        read_only_fields = ('student_id', 'registration_date')
    
    def get_full_name(self, obj):
        """Return student's full name."""
        return f"{obj.first_name} {obj.last_name}"
    
    def validate_email(self, value):
        """Validate email is unique."""
        if self.instance and self.instance.email == value:
            return value
        
        if Student.objects.filter(email=value).exists():
            raise serializers.ValidationError("A student with this email already exists.")
        return value
    
    def validate_phone(self, value):
        """Validate phone number format."""
        if not value.replace('+', '').replace('-', '').isdigit():
            raise serializers.ValidationError("Phone number must contain only digits, + and -")
        return value