from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExamViewSet, ExamScheduleViewSet, ExamResultViewSet, ReportCardViewSet

router = DefaultRouter()
router.register(r'', ExamViewSet)
router.register(r'schedules', ExamScheduleViewSet)
router.register(r'results', ExamResultViewSet)
router.register(r'report-cards', ReportCardViewSet)

urlpatterns = [
    path('', include(router.urls)),
]