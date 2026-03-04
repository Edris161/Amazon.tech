from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from news.views import NewsViewSet
from staff.views import StaffViewSet
from gallery.views import GalleryViewSet
from academics.views import AcademicsViewSet
from admissions.views import AdmissionViewSet
from contact.views import ContactViewSet

router = DefaultRouter()
router.register("news", NewsViewSet)
router.register("staff", StaffViewSet)
router.register("gallery", GalleryViewSet)
router.register("academics", AcademicsViewSet)
router.register("admissions", AdmissionViewSet)
router.register("contact", ContactViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]