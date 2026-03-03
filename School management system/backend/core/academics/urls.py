from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AcademicYearViewSet, ClassViewSet, SectionViewSet, SubjectViewSet, TimetableViewSet

router = DefaultRouter()
router.register(r'academic-years', AcademicYearViewSet)
router.register(r'classes', ClassViewSet)
router.register(r'sections', SectionViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'timetable', TimetableViewSet)

urlpatterns = [
    path('', include(router.urls)),
]