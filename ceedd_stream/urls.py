from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ZoneContributiveViewSet,
    BailleurViewSet,
    TypeInfrastructureViewSet,
    ClientViewSet,
    InfrastructureViewSet,
    FinanceViewSet,
    InspectionViewSet,
    PhotoViewSet,
    UploadShapefileViewSet,
)

router = DefaultRouter()
router.register(r"zones", ZoneContributiveViewSet, basename="zonecontributive")
router.register(r"bailleurs", BailleurViewSet, basename="bailleur")
router.register(
    r"types-infrastructure", TypeInfrastructureViewSet, basename="typeinfrastructure"
)
router.register(r"clients", ClientViewSet, basename="client")
router.register(r"infrastructures", InfrastructureViewSet, basename="infrastructure")
router.register(r"finances", FinanceViewSet, basename="finance")
router.register(r"inspections", InspectionViewSet, basename="inspection")
router.register(r"photos", PhotoViewSet, basename="photo")
router.register(r"shps", UploadShapefileViewSet, basename="shp")

urlpatterns = [
    path("", include(router.urls)),
]
