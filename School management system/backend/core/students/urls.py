from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, ParentViewSet, StudentDocumentViewSet, StudentPromotionViewSet

router = DefaultRouter()
router.register(r'', StudentViewSet)
router.register(r'parents', ParentViewSet)
router.register(r'documents', StudentDocumentViewSet)
router.register(r'promotions', StudentPromotionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]