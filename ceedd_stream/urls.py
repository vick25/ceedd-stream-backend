from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'zonecontributive', views.ZoneContributiveViewSet, basename='zonecontributive')
router.register(r'bailleur', views.BailleurViewSet, basename='bailleur')
router.register(r'typeinfrastructure', views.TypeInfrastructureViewSet, basename='typeinfrastructure')
router.register(r'client', views.ClientViewSet, basename='client')
router.register(r'finance', views.FinanceViewSet, basename='finance')
router.register(r'infrastructure', views.InfrastructureViewSet, basename='infrastructure')
router.register(r'inspection', views.InspectionViewSet, basename='inspection')
router.register(r'photo', views.PhotoViewSet, basename='photo')
#router.register(r'role', views.RoleViewSet, basename='role')
#router.register(r'utilisateur', views.UtilisateurViewSet, basename='utilisateur')

urlpatterns = [
    path('', include(router.urls)),
]