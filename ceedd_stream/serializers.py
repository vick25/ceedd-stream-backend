from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import ZoneContributive, Bailleur, TypeInfrastructure, Client, Infrastructure, Finance, Inspection, Photo

class ZoneContributiveSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = ZoneContributive
        geo_field = "geom"
        fields = '__all__'