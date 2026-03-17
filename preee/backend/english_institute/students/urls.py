from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, LevelViewSet

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'levels', LevelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]