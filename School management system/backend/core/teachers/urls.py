from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeacherViewSet, TeacherAttendanceViewSet, TeacherLeaveViewSet

router = DefaultRouter()
router.register(r'', TeacherViewSet)
router.register(r'attendance', TeacherAttendanceViewSet)
router.register(r'leaves', TeacherLeaveViewSet)

urlpatterns = [
    path('', include(router.urls)),
]