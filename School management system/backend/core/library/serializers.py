from rest_framework import serializers
from django.utils import timezone
from students.serializers import StudentSerializer
from teachers.serializers import TeacherSerializer
from .models import Book, BookIssue, BookReservation

class BookSerializer(serializers.ModelSerializer):
    available_copies_display = serializers.SerializerMethodField()
    cover_image_url = serializers.SerializerMethodField()
    issue_count = serializers.SerializerMethodField()
    reservation_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_available_copies_display(self, obj):
        return f"{obj.available_copies}/{obj.total_copies}"
    
    def get_cover_image_url(self, obj):
        if obj.cover_image:
            return obj.cover_image.url
        return None
    
    def get_issue_count(self, obj):
        return obj.issues.filter(status='issued').count()
    
    def get_reservation_count(self, obj):
        return obj.reservations.filter(status='pending').count()
    
    def validate(self, data):
        if data.get('available_copies', 0) > data.get('total_copies', 0):
            raise serializers.ValidationError(
                "Available copies cannot exceed total copies"
            )
        return data

class BookIssueSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    book_author = serializers.CharField(source='book.author', read_only=True)
    book_isbn = serializers.CharField(source='book.isbn', read_only=True)
    borrower_name = serializers.SerializerMethodField()
    borrower_type = serializers.CharField(source='issued_to', read_only=True)
    issued_by_name = serializers.CharField(source='issued_by.full_name', read_only=True)
    days_overdue = serializers.SerializerMethodField()
    fine_amount_display = serializers.SerializerMethodField()
    
    class Meta:
        model = BookIssue
        fields = '__all__'
        read_only_fields = ['id', 'issue_date', 'created_at', 'issued_by', 'fine_amount']
    
    def get_borrower_name(self, obj):
        if obj.student:
            return obj.student.user.full_name
        elif obj.teacher:
            return obj.teacher.user.full_name
        return "Unknown"
    
    def get_days_overdue(self, obj):
        if obj.status == 'issued' and obj.due_date < timezone.now().date():
            return (timezone.now().date() - obj.due_date).days
        return 0
    
    def get_fine_amount_display(self, obj):
        if obj.fine_amount > 0:
            return f"₹{obj.fine_amount}"
        return "No fine"
    
    def validate(self, data):
        # Check if book is available
        book = data.get('book')
        if book and book.available_copies <= 0:
            raise serializers.ValidationError("No copies available for issue")
        
        # Check if borrower already has book
        if data.get('student'):
            if BookIssue.objects.filter(
                student=data['student'],
                book=book,
                status='issued'
            ).exists():
                raise serializers.ValidationError("Student already has this book issued")
        elif data.get('teacher'):
            if BookIssue.objects.filter(
                teacher=data['teacher'],
                book=book,
                status='issued'
            ).exists():
                raise serializers.ValidationError("Teacher already has this book issued")
        
        return data
    
    def create(self, validated_data):
        validated_data['issued_by'] = self.context['request'].user
        
        # Decrease available copies
        book = validated_data['book']
        book.available_copies -= 1
        book.save()
        
        return super().create(validated_data)

class BookReturnSerializer(serializers.Serializer):
    return_date = serializers.DateField(default=timezone.now().date)
    condition = serializers.ChoiceField(
        choices=[('good', 'Good'), ('damaged', 'Damaged'), ('lost', 'Lost')],
        default='good'
    )
    fine_paid = serializers.BooleanField(default=False)
    remarks = serializers.CharField(required=False, allow_blank=True)

class BookReservationSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    book_author = serializers.CharField(source='book.author', read_only=True)
    book_isbn = serializers.CharField(source='book.isbn', read_only=True)
    reserver_name = serializers.SerializerMethodField()
    reserver_type = serializers.CharField(source='reserved_by', read_only=True)
    
    class Meta:
        model = BookReservation
        fields = '__all__'
        read_only_fields = ['id', 'reservation_date', 'notified']
    
    def get_reserver_name(self, obj):
        if obj.student:
            return obj.student.user.full_name
        elif obj.teacher:
            return obj.teacher.user.full_name
        return "Unknown"
    
    def validate(self, data):
        # Check if already reserved
        book = data.get('book')
        if data.get('student'):
            if BookReservation.objects.filter(
                student=data['student'],
                book=book,
                status='pending'
            ).exists():
                raise serializers.ValidationError("Student already has pending reservation for this book")
        elif data.get('teacher'):
            if BookReservation.objects.filter(
                teacher=data['teacher'],
                book=book,
                status='pending'
            ).exists():
                raise serializers.ValidationError("Teacher already has pending reservation for this book")
        
        return data

class BookSearchSerializer(serializers.Serializer):
    query = serializers.CharField(required=False)
    category = serializers.ChoiceField(choices=Book.CATEGORY_CHOICES, required=False)
    author = serializers.CharField(required=False)
    publisher = serializers.CharField(required=False)
    language = serializers.CharField(required=False)
    available_only = serializers.BooleanField(default=False)

class LibraryStatisticsSerializer(serializers.Serializer):
    total_books = serializers.IntegerField()
    total_copies = serializers.IntegerField()
    available_copies = serializers.IntegerField()
    issued_books = serializers.IntegerField()
    overdue_books = serializers.IntegerField()
    pending_reservations = serializers.IntegerField()
    category_breakdown = serializers.ListField(child=serializers.DictField())
    most_borrowed = serializers.ListField(child=serializers.DictField())