from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'zonecontributive', views.ZoneContributiveViewSet, basename='zonecontributive')

urlpatterns = [
    path('', include(router.urls)),
]