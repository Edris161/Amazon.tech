from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FeeStructureViewSet, FeeAssignmentViewSet, PaymentViewSet, ExpenseViewSet

router = DefaultRouter()
router.register(r'fee-structures', FeeStructureViewSet)
router.register(r'fee-assignments', FeeAssignmentViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'expenses', ExpenseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]