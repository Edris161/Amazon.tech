from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Sum, Avg
from django.utils import timezone
from datetime import timedelta
from assignments import models
from assignments import models
from students.models import Student
from teachers.models import Teacher
from attendance.models import StudentAttendance
from finance.models import Payment, Expense
from exams.models import ExamResult

class DashboardReportView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Get counts
        total_students = Student.objects.filter(is_active=True).count()
        total_teachers = Teacher.objects.filter(is_active=True).count()
        
        # Get today's attendance
        today = timezone.now().date()
        present_today = StudentAttendance.objects.filter(
            date=today, 
            status='present'
        ).count()
        
        # Get monthly revenue
        month_start = timezone.now().replace(day=1)
        monthly_revenue = Payment.objects.filter(
            payment_date__gte=month_start,
            status='completed'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        return Response({
            'total_students': total_students,
            'total_teachers': total_teachers,
            'present_today': present_today,
            'monthly_revenue': monthly_revenue,
            'recent_activities': []  # You can populate this from AuditLog
        })

class StudentReportView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Class-wise student distribution
        class_distribution = Student.objects.filter(
            is_active=True
        ).values(
            'current_class__name'
        ).annotate(
            count=Count('id')
        )
        
        # Gender distribution
        gender_distribution = Student.objects.filter(
            is_active=True
        ).values(
            'gender'
        ).annotate(
            count=Count('id')
        )
        
        return Response({
            'class_distribution': class_distribution,
            'gender_distribution': gender_distribution,
            'total_students': Student.objects.filter(is_active=True).count(),
            'new_admissions': Student.objects.filter(
                admission_date__gte=timezone.now() - timedelta(days=30)
            ).count()
        })

class FinanceReportView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Monthly revenue for last 6 months
        months = []
        revenue_data = []
        
        for i in range(5, -1, -1):
            month = timezone.now() - timedelta(days=30*i)
            month_start = month.replace(day=1)
            if month.month == 12:
                month_end = month.replace(day=31)
            else:
                month_end = month.replace(month=month.month+1, day=1) - timedelta(days=1)
            
            revenue = Payment.objects.filter(
                payment_date__range=[month_start, month_end],
                status='completed'
            ).aggregate(total=Sum('amount'))['total'] or 0
            
            months.append(month.strftime('%B %Y'))
            revenue_data.append(float(revenue))
        
        # Expense by category
        expense_by_category = Expense.objects.filter(
            expense_date__year=timezone.now().year
        ).values(
            'category'
        ).annotate(
            total=Sum('amount')
        )
        
        return Response({
            'monthly_revenue': {
                'months': months,
                'data': revenue_data
            },
            'expense_by_category': expense_by_category,
            'total_revenue': Payment.objects.filter(
                status='completed'
            ).aggregate(total=Sum('amount'))['total'] or 0,
            'pending_fees': 0  # Calculate from FeeAssignment
        })

class AttendanceReportView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Get date range from query params
        days = int(request.GET.get('days', 30))
        start_date = timezone.now().date() - timedelta(days=days)
        
        # Daily attendance for the period
        attendance_data = StudentAttendance.objects.filter(
            date__gte=start_date
        ).values(
            'date'
        ).annotate(
            present=Count('id', filter=models.Q(status='present')),
            absent=Count('id', filter=models.Q(status='absent')),
            late=Count('id', filter= models.Q(status='late'))
        ).order_by('date')
        
        # Overall statistics
        total_days = StudentAttendance.objects.filter(
            date__gte=start_date
        ).values('date').distinct().count()
        
        avg_attendance = StudentAttendance.objects.filter(
            date__gte=start_date,
            status='present'
        ).count() / (Student.objects.filter(is_active=True).count() * total_days) * 100 if total_days > 0 else 0
        
        return Response({
            'daily_data': attendance_data,
            'average_attendance': round(avg_attendance, 2),
            'total_days': total_days,
            'period_days': days
        })

class ExportReportView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        report_type = request.GET.get('type', 'student')
        format_type = request.GET.get('format', 'csv')
        
        # Generate different reports based on type
        if report_type == 'student':
            data = self.get_student_data()
        elif report_type == 'attendance':
            data = self.get_attendance_data()
        elif report_type == 'finance':
            data = self.get_finance_data()
        else:
            data = {}
        
        # In a real app, you'd generate CSV/PDF here
        return Response({
            'report_type': report_type,
            'format': format_type,
            'data': data,
            'message': f'{report_type} report generated successfully'
        })
    
    def get_student_data(self):
        return Student.objects.filter(is_active=True).values(
            'user__first_name', 'user__last_name', 'admission_number',
            'current_class__name', 'current_section__name'
        )[:100]
    
    def get_attendance_data(self):
        return StudentAttendance.objects.filter(
            date=timezone.now().date()
        ).values(
            'student__user__first_name', 'student__user__last_name',
            'student__admission_number', 'status'
        )[:100]
    
    def get_finance_data(self):
        return Payment.objects.filter(
            status='completed'
        ).values(
            'student__user__first_name', 'student__user__last_name',
            'amount', 'payment_date', 'receipt_number'
        )[:100]