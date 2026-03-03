from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.DashboardReportView.as_view(), name='dashboard-report'),
    path('students/', views.StudentReportView.as_view(), name='student-report'),
    path('finance/', views.FinanceReportView.as_view(), name='finance-report'),
    path('attendance/', views.AttendanceReportView.as_view(), name='attendance-report'),
    path('export/', views.ExportReportView.as_view(), name='export-report'),
]