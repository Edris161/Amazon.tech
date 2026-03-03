from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentAttendanceViewSet, BulkAttendanceViewSet, HolidayViewSet

router = DefaultRouter()
router.register(r'student', StudentAttendanceViewSet)
router.register(r'bulk', BulkAttendanceViewSet)
router.register(r'holidays', HolidayViewSet)

urlpatterns = [
    path('', include(router.urls)),
]