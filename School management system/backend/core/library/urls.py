from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, BookIssueViewSet, BookReservationViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'issues', BookIssueViewSet)
router.register(r'reservations', BookReservationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]