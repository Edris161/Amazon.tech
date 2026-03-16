# classes/serializers.py
from rest_framework import serializers
from .models import ClassRoom, Enrollment
from students.models import Level

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'

class ClassRoomSerializer(serializers.ModelSerializer):
    # Field to show level name instead of ID in GET requests
    level_name = serializers.ReadOnlyField(source='level.name')

    class Meta:
        model = ClassRoom
        fields = ['id', 'name', 'level', 'level_name', 'teacher_name', 
                  'schedule', 'capacity', 'is_active']
