from rest_framework import serializers
from accounts.serializers import UserSerializer
from academics.serializers import ClassSerializer, SectionSerializer, AcademicYearSerializer
from .models import Student, Parent, StudentDocument, StudentPromotion

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    current_class = ClassSerializer(read_only=True)
    current_class_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    current_section = SectionSerializer(read_only=True)
    current_section_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    academic_year = AcademicYearSerializer(read_only=True)
    academic_year_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    parent_count = serializers.IntegerField(source='parents.count', read_only=True)
    
    class Meta:
        model = Student
        fields = '__all__'
        read_only_fields = ['id', 'admission_date', 'created_at', 'updated_at']
    
    def validate(self, data):
        if data.get('current_class_id') and not data.get('current_section_id'):
            raise serializers.ValidationError(
                {"current_section_id": "Section is required when class is selected"}
            )
        return data
    
    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        class_id = validated_data.pop('current_class_id', None)
        section_id = validated_data.pop('current_section_id', None)
        academic_year_id = validated_data.pop('academic_year_id', None)
        
        student = Student.objects.create(
            user_id=user_id,
            current_class_id=class_id,
            current_section_id=section_id,
            academic_year_id=academic_year_id,
            **validated_data
        )
        return student
    
    def update(self, instance, validated_data):
        if 'current_class_id' in validated_data:
            instance.current_class_id = validated_data.pop('current_class_id')
        if 'current_section_id' in validated_data:
            instance.current_section_id = validated_data.pop('current_section_id')
        if 'academic_year_id' in validated_data:
            instance.academic_year_id = validated_data.pop('academic_year_id')
        
        return super().update(instance, validated_data)

class ParentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    students = StudentSerializer(many=True, read_only=True)
    student_ids = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(),
        many=True,
        write_only=True,
        required=False,
        source='students'
    )
    children_count = serializers.IntegerField(source='students.count', read_only=True)
    
    class Meta:
        model = Parent
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        student_ids = validated_data.pop('students', [])
        user_id = validated_data.pop('user_id')
        
        parent = Parent.objects.create(user_id=user_id, **validated_data)
        
        if student_ids:
            parent.students.set(student_ids)
        
        return parent
    
    def update(self, instance, validated_data):
        if 'students' in validated_data:
            instance.students.set(validated_data.pop('students'))
        return super().update(instance, validated_data)

class StudentDocumentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.full_name', read_only=True)
    verified_by_name = serializers.CharField(source='verified_by.full_name', read_only=True)
    document_url = serializers.SerializerMethodField()
    
    class Meta:
        model = StudentDocument
        fields = '__all__'
        read_only_fields = ['id', 'uploaded_at', 'verified_by', 'verified']
    
    def get_document_url(self, obj):
        if obj.file:
            return obj.file.url
        return None
    
    def create(self, validated_data):
        validated_data['verified'] = False
        return super().create(validated_data)

class StudentPromotionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.full_name', read_only=True)
    from_class_name = serializers.CharField(source='from_class.name', read_only=True)
    to_class_name = serializers.CharField(source='to_class.name', read_only=True)
    from_section_name = serializers.CharField(source='from_section.name', read_only=True)
    to_section_name = serializers.CharField(source='to_section.name', read_only=True)
    academic_year_name = serializers.CharField(source='academic_year.name', read_only=True)
    promoted_by_name = serializers.CharField(source='promoted_by.full_name', read_only=True)
    
    class Meta:
        model = StudentPromotion
        fields = '__all__'
        read_only_fields = ['id', 'promoted_on', 'promoted_by']

class StudentBulkUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    
    def validate_file(self, value):
        if not value.name.endswith(('.csv', '.xlsx')):
            raise serializers.ValidationError("File must be CSV or Excel format")
        return value

class StudentSearchSerializer(serializers.Serializer):
    query = serializers.CharField(required=False)
    class_id = serializers.IntegerField(required=False)
    section_id = serializers.IntegerField(required=False)
    is_active = serializers.BooleanField(required=False)
    gender = serializers.ChoiceField(choices=['M', 'F', 'O'], required=False)