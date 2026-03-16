# students/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet

router = DefaultRouter()
router.register(r'', StudentViewSet) # This registers the /api/students/ endpoint

urlpatterns = [
    path('api/students/', include(router.urls)),
]
