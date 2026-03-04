from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse


# Optional: API root endpoint
def api_root(request):
    return JsonResponse({
        "message": "School Management System API",
        "endpoints": {
            "news": "/api/news/",
            "staff": "/api/staff/",
            "teachers": "/api/teachers/",
            "academics": "/api/academics/",
            "gallery": "/api/gallery/",
            "admissions": "/api/admissions/",
            "contact": "/api/contact/",
            "settings": "/api/settings/",
        }
    })


urlpatterns = [

    # Admin Panel
    path("admin/", admin.site.urls),

    # API Root
    path("api/", api_root),

    # API Apps
    path("api/news/", include("news.urls")),
    path("api/staff/", include("staff.urls")),
    path("api/teachers/", include("teachers.urls")),
    path("api/academics/", include("academics.urls")),
    path("api/gallery/", include("gallery.urls")),
    path("api/admissions/", include("admissions.urls")),
    path("api/contact/", include("contact.urls")),
    path("api/settings/", include("core.urls")),
]


# Serve media & static files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)