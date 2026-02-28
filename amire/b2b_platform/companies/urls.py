from django.urls import path
from .views import CompanyListView, CompanyDetailView

urlpatterns = [
    path('', CompanyListView.as_view(), name='company-list'),
    path('<slug:slug>/', CompanyDetailView.as_view(), name='company-detail'),
]