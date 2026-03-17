from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClassViewSet, EnrollmentViewSet

router = DefaultRouter()
router.register(r'classes', ClassViewSet)
router.register(r'enrollments', EnrollmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]