from django.urls import path
from .views import AdmissionApplicationCreateView

urlpatterns = [
    path("apply/", AdmissionApplicationCreateView.as_view(), name="apply-admission"),
]