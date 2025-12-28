"""
URL configuration for ceedd_stream_api project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from ceedd_stream.views import (
    UserCreateView,
    UserRetrieveView,
    CustomTokenObtainPairView,
    get_volume_by_date,
    get_volume_by_filters,
    get_photos_for_object,
)
from rest_framework_simplejwt.views import TokenRefreshView

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="CEEDD Stream API",
        default_version="v1",
        description="API for managing CEEDD Stream data",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="vickadiata@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Documentation
urlpatterns = [
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

urlpatterns += [
    path("admin/", admin.site.urls),
    # User endpoints
    path("api/users/register/", UserCreateView.as_view(), name="register"),
    path("api/users/<int:pk>/", UserRetrieveView.as_view(), name="user-detail"),
    # Authentication endpoints
    path("api/token/", CustomTokenObtainPairView.as_view(), name="get_token"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="refresh_token"),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    # API endpoints
    path("api/v1/", include("ceedd_stream.urls")),
    # Stats
    path("api/infras/volume", get_volume_by_filters, name="get_volume_by_filters"),
    path("api/infras/volume_by_date", get_volume_by_date, name="get_volume_by_date"),
    # Photos by object
    path(
        "api/photos/by_object/",
        get_photos_for_object,
        name="get_photos_for_object",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
