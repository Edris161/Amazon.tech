from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

# Import ViewSets
from news.views import NewsViewSet
from staff.views import StaffViewSet
from gallery.views import GalleryViewSet
from academics.views import AcademicsViewSet
from admissions.views import AdmissionViewSet
from contact.views import ContactViewSet


# API Router
router = DefaultRouter()

router.register(r"news", NewsViewSet, basename="news")
router.register(r"staff", StaffViewSet, basename="staff")
router.register(r"gallery", GalleryViewSet, basename="gallery")
router.register(r"academics", AcademicsViewSet, basename="academics")
router.register(r"admissions", AdmissionViewSet, basename="admissions")
router.register(r"contact", ContactViewSet, basename="contact")


# URL Patterns
urlpatterns = [
    path("admin/", admin.site.urls),

    # API Routes
    path("api/", include(router.urls)),
]


# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)