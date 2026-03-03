from rest_framework import serializers
from django.utils import timezone
from students.serializers import StudentSerializer
from academics.serializers import ClassSerializer, SectionSerializer, AcademicYearSerializer
from .models import StudentAttendance, BulkAttendance, Holiday
from academics.models import AcademicYear, Class, Section

class StudentAttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.full_name', read_only=True)
    student_roll = serializers.CharField(source='student.roll_number', read_only=True)
    student_admission = serializers.CharField(source='student.admission_number', read_only=True)
    class_name = serializers.CharField(source='class_group.name', read_only=True)
    section_name = serializers.CharField(source='section.name', read_only=True)
    marked_by_name = serializers.CharField(source='marked_by.full_name', read_only=True)
    
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
    academic_year_id = serializers.PrimaryKeyRelatedField(
        queryset=AcademicYear.objects.all(),
        source='academic_year',
        write_only=True
    )
    
    class Meta:
        model = StudentAttendance
        fields = '__all__'
        read_only_fields = ['id', 'marked_at', 'marked_by']
    
    def validate(self, data):
        # Check for duplicate attendance
        if StudentAttendance.objects.filter(
            student=data['student'],
            date=data['date']
        ).exists() and not self.instance:
            raise serializers.ValidationError(
                "Attendance already marked for this student on this date"
            )
        return data
    
    def create(self, validated_data):
        validated_data['marked_by'] = self.context['request'].user
        return super().create(validated_data)

class BulkAttendanceSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source='class_group.name', read_only=True)
    section_name = serializers.CharField(source='section.name', read_only=True)
    marked_by_name = serializers.CharField(source='marked_by.full_name', read_only=True)
    
    class Meta:
        model = BulkAttendance
        fields = '__all__'
        read_only_fields = ['id', 'marked_at', 'marked_by']
    
    def create(self, validated_data):
        validated_data['marked_by'] = self.context['request'].user
        return super().create(validated_data)

class HolidaySerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source='class_group.name', read_only=True, allow_null=True)
    academic_year_name = serializers.CharField(source='academic_year.name', read_only=True)
    
    class_id = serializers.PrimaryKeyRelatedField(
        queryset=Class.objects.all(),
        source='class_group',
        write_only=True,
        required=False,
        allow_null=True
    )
    academic_year_id = serializers.PrimaryKeyRelatedField(
        queryset=AcademicYear.objects.all(),
        source='academic_year',
        write_only=True
    )
    
    class Meta:
        model = Holiday
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
    
    def validate(self, data):
        # Check for duplicate holiday
        if Holiday.objects.filter(
            name=data['name'],
            date=data['date']
        ).exists() and not self.instance:
            raise serializers.ValidationError(
                "Holiday with this name already exists on this date"
            )
        return data

class DailyAttendanceSummarySerializer(serializers.Serializer):
    date = serializers.DateField()
    total_students = serializers.IntegerField()
    present = serializers.IntegerField()
    absent = serializers.IntegerField()
    late = serializers.IntegerField()
    half_day = serializers.IntegerField()
    percentage = serializers.FloatField()

class MonthlyAttendanceReportSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    student_name = serializers.CharField()
    roll_number = serializers.CharField()
    class_name = serializers.CharField()
    section_name = serializers.CharField()
    total_days = serializers.IntegerField()
    present_days = serializers.IntegerField()
    absent_days = serializers.IntegerField()
    late_days = serializers.IntegerField()
    half_days = serializers.IntegerField()
    attendance_percentage = serializers.FloatField()