from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import ZoneContributive, Bailleur, TypeInfrastructure, Client, Infrastructure, Finance, Inspection, Photo

class ZoneContributiveSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = ZoneContributive
        geo_field = "geom"
        fields = '__all__'

class BailleurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bailleur
        fields = '__all__'

class TypeInfrastructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeInfrastructure
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class FinanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finance
        fields = '__all__'

class InfrastructureSerializer(serializers.ModelSerializer):
    finances = BailleurSerializer(many=True, read_only=True)
    class Meta:
        model = Infrastructure
        fields = '__all__'

class InspectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inspection
        fields = '__all__'

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'