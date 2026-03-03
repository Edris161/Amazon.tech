from rest_framework import serializers
from django.db.models import Avg, Sum
from academics.models import Subject, AcademicYear, Class
from academics.serializers import ClassSerializer, SubjectSerializer, AcademicYearSerializer
from students.serializers import StudentSerializer
from .models import Exam, ExamSchedule, ExamResult, ReportCard

class ExamSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source='class_group.name', read_only=True)
    academic_year_name = serializers.CharField(source='academic_year.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    schedule_count = serializers.IntegerField(source='schedules.count', read_only=True)
    
    class_id = serializers.PrimaryKeyRelatedField(
        queryset=Class.objects.all(),
        source='class_group',
        write_only=True
    )
    academic_year_id = serializers.PrimaryKeyRelatedField(
        queryset=AcademicYear.objects.all(),
        source='academic_year',
        write_only=True
    )
    
    class Meta:
        model = Exam
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'created_by']
    
    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("Start date cannot be after end date")
        return data
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

class ExamScheduleSerializer(serializers.ModelSerializer):
    exam_name = serializers.CharField(source='exam.name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    subject_code = serializers.CharField(source='subject.code', read_only=True)
    
    exam_id = serializers.PrimaryKeyRelatedField(
        queryset=Exam.objects.all(),
        source='exam',
        write_only=True
    )
    subject_id = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(),
        source='subject',
        write_only=True
    )
    
    class Meta:
        model = ExamSchedule
        fields = '__all__'
        read_only_fields = ['id']
    
    def validate(self, data):
        # Check if schedule already exists for this exam and subject
        if ExamSchedule.objects.filter(
            exam=data['exam'],
            subject=data['subject']
        ).exists() and not self.instance:
            raise serializers.ValidationError(
                "Schedule already exists for this subject in this exam"
            )
        
        # Check if date is within exam period
        exam = data['exam']
        if data['date'] < exam.start_date or data['date'] > exam.end_date:
            raise serializers.ValidationError(
                "Schedule date must be within exam period"
            )
        
        return data

class ExamResultSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.full_name', read_only=True)
    student_roll = serializers.CharField(source='student.roll_number', read_only=True)
    exam_name = serializers.CharField(source='exam_schedule.exam.name', read_only=True)
    subject_name = serializers.CharField(source='exam_schedule.subject.name', read_only=True)
    subject_code = serializers.CharField(source='exam_schedule.subject.code', read_only=True)
    max_marks = serializers.IntegerField(source='exam_schedule.max_marks', read_only=True)
    pass_marks = serializers.IntegerField(source='exam_schedule.pass_marks', read_only=True)
    entered_by_name = serializers.CharField(source='entered_by.user.full_name', read_only=True)
    percentage = serializers.SerializerMethodField()
    result_status = serializers.SerializerMethodField()
    
    class Meta:
        model = ExamResult
        fields = '__all__'
        read_only_fields = ['id', 'entered_at', 'updated_at', 'entered_by', 'grade']
    
    def get_percentage(self, obj):
        return round((obj.marks_obtained / obj.exam_schedule.max_marks) * 100, 2)
    
    def get_result_status(self, obj):
        if obj.marks_obtained >= obj.exam_schedule.pass_marks:
            return 'PASS'
        return 'FAIL'
    
    def validate(self, data):
        # Check if result already exists
        if ExamResult.objects.filter(
            exam_schedule=data['exam_schedule'],
            student=data['student']
        ).exists() and not self.instance:
            raise serializers.ValidationError(
                "Result already exists for this student in this exam"
            )
        
        # Validate marks
        if data['marks_obtained'] > data['exam_schedule'].max_marks:
            raise serializers.ValidationError(
                f"Marks cannot exceed {data['exam_schedule'].max_marks}"
            )
        
        if data['marks_obtained'] < 0:
            raise serializers.ValidationError("Marks cannot be negative")
        
        return data
    
    def create(self, validated_data):
        validated_data['entered_by'] = self.context['request'].user.teacher_profile
        return super().create(validated_data)

class ExamResultBulkSerializer(serializers.Serializer):
    exam_schedule_id = serializers.IntegerField()
    results = serializers.ListField(
        child=serializers.DictField()
    )
    
    def validate_results(self, value):
        for result in value:
            if 'student_id' not in result or 'marks_obtained' not in result:
                raise serializers.ValidationError(
                    "Each result must have student_id and marks_obtained"
                )
        return value

class ReportCardSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.full_name', read_only=True)
    student_roll = serializers.CharField(source='student.roll_number', read_only=True)
    student_class = serializers.CharField(source='student.current_class.name', read_only=True)
    student_section = serializers.CharField(source='student.current_section.name', read_only=True)
    exam_name = serializers.CharField(source='exam.name', read_only=True)
    generated_by_name = serializers.CharField(source='generated_by.full_name', read_only=True)
    pdf_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ReportCard
        fields = '__all__'
        read_only_fields = ['id', 'generated_at', 'generated_by']
    
    def get_pdf_url(self, obj):
        if obj.pdf_file:
            return obj.pdf_file.url
        return None

class ExamResultSummarySerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    student_name = serializers.CharField()
    roll_number = serializers.CharField()
    total_marks = serializers.FloatField()
    percentage = serializers.FloatField()
    grade = serializers.CharField()
    rank = serializers.IntegerField()
    subjects = serializers.ListField(child=serializers.DictField())