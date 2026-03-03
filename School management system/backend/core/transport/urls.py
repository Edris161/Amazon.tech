from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransportRouteViewSet, TransportStopViewSet, VehicleViewSet, TransportAssignmentViewSet

router = DefaultRouter()
router.register(r'routes', TransportRouteViewSet)
router.register(r'stops', TransportStopViewSet)
router.register(r'vehicles', VehicleViewSet)
router.register(r'assignments', TransportAssignmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]