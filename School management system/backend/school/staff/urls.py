from rest_framework.routers import DefaultRouter
from .views import TeacherViewSet

router = DefaultRouter()
router.register(r"", TeacherViewSet, basename="staff")

urlpatterns = router.urls