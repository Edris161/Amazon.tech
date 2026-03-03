from rest_framework import serializers
from django.utils import timezone
from academics.serializers import ClassSerializer, SectionSerializer, SubjectSerializer
from teachers.models import Teacher
from teachers.serializers import TeacherSerializer
from students.serializers import StudentSerializer
from .models import Assignment, Submission
from academics.models import Subject, Section, Class

class AssignmentSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source='class_group.name', read_only=True)
    section_name = serializers.CharField(source='section.name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    teacher_name = serializers.CharField(source='teacher.user.full_name', read_only=True)
    submission_count = serializers.IntegerField(source='submissions.count', read_only=True)
    graded_count = serializers.SerializerMethodField()
    attachment_url = serializers.SerializerMethodField()
    
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
    
    class Meta:
        model = Assignment
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_attachment_url(self, obj):
        if obj.attachment:
            return obj.attachment.url
        return None
    
    def get_graded_count(self, obj):
        return obj.submissions.filter(status='graded').count()
    
    def validate_due_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Due date cannot be in the past")
        return value

class SubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.full_name', read_only=True)
    student_roll = serializers.CharField(source='student.roll_number', read_only=True)
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)
    assignment_subject = serializers.CharField(source='assignment.subject.name', read_only=True)
    graded_by_name = serializers.CharField(source='graded_by.user.full_name', read_only=True)
    attachment_url = serializers.SerializerMethodField()
    is_late = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Submission
        fields = '__all__'
        read_only_fields = ['id', 'submission_date', 'graded_by', 'graded_at', 'status']
    
    def get_attachment_url(self, obj):
        if obj.attachment:
            return obj.attachment.url
        return None
    
    def validate(self, data):
        # Check if submission already exists
        if Submission.objects.filter(
            assignment=data['assignment'],
            student=data['student']
        ).exists() and not self.instance:
            raise serializers.ValidationError(
                "Submission already exists for this assignment"
            )
        return data

class SubmissionGradeSerializer(serializers.Serializer):
    marks_obtained = serializers.DecimalField(max_digits=5, decimal_places=2)
    feedback = serializers.CharField(required=False, allow_blank=True)

class AssignmentBulkCreateSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    assignment_type = serializers.ChoiceField(choices=Assignment.ASSIGNMENT_TYPES)
    class_ids = serializers.ListField(child=serializers.IntegerField())
    section_ids = serializers.ListField(child=serializers.IntegerField())
    subject_id = serializers.IntegerField()
    due_date = serializers.DateTimeField()
    max_marks = serializers.IntegerField(default=100)
    instructions = serializers.CharField(required=False, allow_blank=True)