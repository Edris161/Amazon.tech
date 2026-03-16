from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClassRoomViewSet, EnrollmentViewSet

router = DefaultRouter()
router.register(r'list', ClassRoomViewSet)
router.register(r'enrollments', EnrollmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
