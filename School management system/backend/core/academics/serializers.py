from rest_framework import serializers
from .models import AcademicYear, Class, Section, Subject, Timetable

class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = ['id', 'name', 'start_date', 'end_date', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def validate(self, data):
        if data.get('is_active'):
            # Deactivate other academic years
            AcademicYear.objects.filter(is_active=True).update(is_active=False)
        return data

class ClassSerializer(serializers.ModelSerializer):
    section_count = serializers.IntegerField(source='sections.count', read_only=True)
    student_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Class
        fields = ['id', 'name', 'code', 'display_order', 'is_active', 
                  'created_at', 'section_count', 'student_count']
        read_only_fields = ['id', 'created_at']
    
    def get_student_count(self, obj):
        from students.models import Student
        return Student.objects.filter(current_class=obj, is_active=True).count()

class SectionSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source='class_group.name', read_only=True)
    class_id = serializers.PrimaryKeyRelatedField(
        queryset=Class.objects.all(),
        source='class_group',
        write_only=True
    )
    student_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Section
        fields = ['id', 'class_group', 'class_name', 'class_id', 'name', 
                  'capacity', 'is_active', 'created_at', 'student_count']
        read_only_fields = ['id', 'created_at']
    
    def get_student_count(self, obj):
        from students.models import Student
        return Student.objects.filter(
            current_class=obj.class_group,
            current_section=obj,
            is_active=True
        ).count()
    
    def validate(self, data):
        # Check if section with same name exists in the class
        if Section.objects.filter(
            class_group=data.get('class_group'),
            name=data.get('name')
        ).exists() and not self.instance:
            raise serializers.ValidationError(
                f"Section {data.get('name')} already exists in this class"
            )
        return data

class SubjectSerializer(serializers.ModelSerializer):
    class_ids = serializers.PrimaryKeyRelatedField(
        queryset=Class.objects.all(),
        many=True,
        write_only=True,
        required=False,
        source='classes'
    )
    classes = ClassSerializer(many=True, read_only=True)
    teacher_count = serializers.IntegerField(source='teachers.count', read_only=True)
    
    class Meta:
        model = Subject
        fields = ['id', 'name', 'code', 'subject_type', 'classes', 'class_ids',
                  'max_marks', 'pass_marks', 'is_active', 'created_at', 'teacher_count']
        read_only_fields = ['id', 'created_at']
    
    def create(self, validated_data):
        class_ids = validated_data.pop('classes', [])
        subject = Subject.objects.create(**validated_data)
        if class_ids:
            subject.classes.set(class_ids)
        return subject
    
    def update(self, instance, validated_data):
        if 'classes' in validated_data:
            instance.classes.set(validated_data.pop('classes'))
        return super().update(instance, validated_data)

class TimetableSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source='class_group.name', read_only=True)
    section_name = serializers.CharField(source='section.name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    teacher_name = serializers.CharField(source='teacher.user.full_name', read_only=True)
    
    class_id = serializers.PrimaryKeyRelatedField(
        queryset=Class.objects.all(),
        source='class_group',
        write_only=True
    )
    section_id = serializers.PrimaryKeyRelatedField(
        queryset=Section.objects.all(),
        source='section',
        write_only=True
    )
    subject_id = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(),
        source='subject',
        write_only=True
    )
    teacher_id = serializers.PrimaryKeyRelatedField(
        queryset=Teacher.objects.all(),
        source='teacher',
        write_only=True
    )
    academic_year_id = serializers.PrimaryKeyRelatedField(
        queryset=AcademicYear.objects.all(),
        source='academic_year',
        write_only=True
    )
    
    class Meta:
        model = Timetable
        fields = [
            'id', 'class_group', 'class_name', 'class_id',
            'section', 'section_name', 'section_id',
            'subject', 'subject_name', 'subject_id',
            'teacher', 'teacher_name', 'teacher_id',
            'academic_year', 'academic_year_id',
            'day', 'start_time', 'end_time', 'room',
            'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def validate(self, data):
        # Check for time conflicts
        conflicts = Timetable.objects.filter(
            class_group=data.get('class_group'),
            section=data.get('section'),
            day=data.get('day'),
            academic_year=data.get('academic_year'),
            start_time__lt=data.get('end_time'),
            end_time__gt=data.get('start_time')
        )
        
        if self.instance:
            conflicts = conflicts.exclude(id=self.instance.id)
        
        if conflicts.exists():
            raise serializers.ValidationError(
                "Time slot conflicts with existing timetable entry"
            )
        
        # Check teacher availability
        teacher_conflicts = Timetable.objects.filter(
            teacher=data.get('teacher'),
            day=data.get('day'),
            academic_year=data.get('academic_year'),
            start_time__lt=data.get('end_time'),
            end_time__gt=data.get('start_time')
        )
        
        if self.instance:
            teacher_conflicts = teacher_conflicts.exclude(id=self.instance.id)
        
        if teacher_conflicts.exists():
            raise serializers.ValidationError(
                "Teacher is not available at this time"
            )
        
        return data

class TimetableBulkSerializer(serializers.Serializer):
    class_id = serializers.IntegerField()
    section_id = serializers.IntegerField()
    academic_year_id = serializers.IntegerField()
    entries = serializers.ListField(
        child=serializers.DictField()
    )
    
    def validate(self, data):
        if not data['entries']:
            raise serializers.ValidationError("At least one timetable entry required")
        return data