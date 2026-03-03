from rest_framework import serializers
from accounts.serializers import UserSerializer
from academics.serializers import ClassSerializer
from students.serializers import StudentSerializer
from teachers.serializers import TeacherSerializer
from teachers.models import Teacher
from students.models import Student
from academics.models import Class
from .models import Announcement, Message, Notification
from django.utils import timezone
from accounts.models import Role

class AnnouncementSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    target_roles_display = serializers.SerializerMethodField()
    target_classes_display = serializers.SerializerMethodField()
    attachment_url = serializers.SerializerMethodField()
    is_active_display = serializers.SerializerMethodField()
    
    target_role_ids = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(),
        many=True,
        write_only=True,
        required=False,
        source='target_roles'
    )
    target_class_ids = serializers.PrimaryKeyRelatedField(
        queryset=Class.objects.all(),
        many=True,
        write_only=True,
        required=False,
        source='target_classes'
    )
    target_student_ids = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(),
        many=True,
        write_only=True,
        required=False,
        source='target_students'
    )
    target_teacher_ids = serializers.PrimaryKeyRelatedField(
        queryset=Teacher.objects.all(),
        many=True,
        write_only=True,
        required=False,
        source='target_teachers'
    )
    
    class Meta:
        model = Announcement
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']
    
    def get_target_roles_display(self, obj):
        if obj.target_all:
            return ['All Users']
        return [role.get_name_display() for role in obj.target_roles.all()]
    
    def get_target_classes_display(self, obj):
        if obj.target_all:
            return ['All Classes']
        return [cls.name for cls in obj.target_classes.all()]
    
    def get_attachment_url(self, obj):
        if obj.attachment:
            return obj.attachment.url
        return None
    
    def get_is_active_display(self, obj):
        now = timezone.now()
        if obj.publish_from > now:
            return 'scheduled'
        elif obj.publish_until and obj.publish_until < now:
            return 'expired'
        elif obj.is_active:
            return 'active'
        return 'inactive'
    
    def validate(self, data):
        if data.get('publish_from') and data.get('publish_until'):
            if data['publish_from'] > data['publish_until']:
                raise serializers.ValidationError(
                    "Publish from date cannot be after publish until date"
                )
        return data
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.full_name', read_only=True)
    recipient_name = serializers.CharField(source='recipient.full_name', read_only=True)
    sender_email = serializers.EmailField(source='sender.email', read_only=True)
    recipient_email = serializers.EmailField(source='recipient.email', read_only=True)
    attachment_url = serializers.SerializerMethodField()
    is_outgoing = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['id', 'sent_at', 'sender', 'is_read', 'read_at']
    
    def get_attachment_url(self, obj):
        if obj.attachment:
            return obj.attachment.url
        return None
    
    def get_is_outgoing(self, obj):
        request = self.context.get('request')
        if request and request.user:
            return obj.sender == request.user
        return False
    
    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user
        return super().create(validated_data)

class MessageThreadSerializer(serializers.Serializer):
    other_user = UserSerializer()
    last_message = MessageSerializer()
    unread_count = serializers.IntegerField()
    total_messages = serializers.IntegerField()

class NotificationSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    time_ago = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'user']
    
    def get_time_ago(self, obj):
        from django.utils.timesince import timesince
        from django.utils import timezone
        return timesince(obj.created_at, timezone.now())

class BulkMessageSerializer(serializers.Serializer):
    recipient_ids = serializers.ListField(child=serializers.IntegerField())
    subject = serializers.CharField(max_length=255)
    content = serializers.CharField()
    send_email = serializers.BooleanField(default=False)
    send_sms = serializers.BooleanField(default=False)