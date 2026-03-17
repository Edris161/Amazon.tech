"""
Classes serializers module.
Handles serialization of Class and Enrollment data.
"""

from rest_framework import serializers
from .models import Class, Enrollment
from students.serializers import StudentSerializer

class ClassSerializer(serializers.ModelSerializer):
    """
    Serializer for Class model.
    Includes enrollment statistics.
    """
    
    level_name = serializers.CharField(source='level.name', read_only=True)
    current_enrollment = serializers.IntegerField(read_only=True)
    available_spots = serializers.IntegerField(read_only=True)
    is_full = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Class
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    
    def validate(self, data):
        """
        Validate that end_date is after start_date.
        """
        if data.get('start_date') and data.get('end_date'):
            if data['end_date'] <= data['start_date']:
                raise serializers.ValidationError(
                    "End date must be after start date"
                )
        return data

class EnrollmentSerializer(serializers.ModelSerializer):
    """
    Serializer for Enrollment model.
    Includes nested student and class details.
    """
    
    student_details = StudentSerializer(source='student', read_only=True)
    class_details = ClassSerializer(source='class_enrolled', read_only=True)
    student_name = serializers.CharField(source='student.__str__', read_only=True)
    class_name = serializers.CharField(source='class_enrolled.name', read_only=True)
    
    class Meta:
        model = Enrollment
        fields = '__all__'
        read_only_fields = ('enrollment_date',)
    
    def validate(self, data):
        """
        Validate enrollment constraints.
        """
        if not self.instance:  # New enrollment
            class_enrolled = data.get('class_enrolled')
            
            if class_enrolled and class_enrolled.is_full:
                # Allow waitlisting but not direct enrollment
                if data.get('status') == 'enrolled':
                    raise serializers.ValidationError(
                        "Class is full. Student will be waitlisted."
                    )
        return data