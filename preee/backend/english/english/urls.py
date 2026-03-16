# institute_management/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # JWT Auth Endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # App Endpoints
    path('api/users/', include('users.urls')),
    path('api/students/', include('students.urls')),
    path('api/classes/', include('classes.urls')),
    path('api/finance/', include('finance.urls')),
]
