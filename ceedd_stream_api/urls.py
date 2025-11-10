from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from ceedd_stream.views import UserCreateView, UserRetrieveView, CustomTokenObtainPairView

schema_view = get_schema_view(
   openapi.Info(
      title="CEEDD Stream API",
      default_version='v1',
      description="STREAM est une application web de suivi et de gestion des infrastructures de gestion des eaux pluviales en milieu urbain.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="vickadiata@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
   path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += [
   path('admin/', admin.site.urls),

   # User endpoints
   path('api/users/register/', UserCreateView.as_view(), name='register'),
   path('api/users/<int:pk>/', UserRetrieveView.as_view(), name='user-detail'),

   # Authentication endpoints
   path('api/token/', CustomTokenObtainPairView.as_view(), name='get_token'),
   path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
   path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
   
   # API endpoints
   path('api/v1/', include('ceedd_stream.urls')),
]
