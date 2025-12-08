from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import (
    ZoneContributive,
    Bailleur,
    TypeInfrastructure,
    Client,
    Infrastructure,
    Finance,
    Inspection,
    Photo,
    Shp,
)


class FinanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finance
        fields = "__all__"


class BailleurSerializer(serializers.ModelSerializer):
    finances = FinanceSerializer(many=True, read_only=True)

    class Meta:
        model = Bailleur
        fields = "__all__"


class TypeInfrastructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeInfrastructure
        fields = "__all__"


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class InfrastructureSerializer(serializers.ModelSerializer):
    # finances = FinanceSerializer(many=True, read_only=True)
    client = ClientSerializer(read_only=True)
    type_infrastructure = TypeInfrastructureSerializer(read_only=True)
    infrastructure_finances = serializers.SerializerMethodField()
    inspections = serializers.SerializerMethodField()

    class Meta:
        model = Infrastructure
        fields = "__all__"

    def get_infrastructure_finances(self, obj):
        # finances = Finance.objects.filter(infrastructure=obj)
        finances = obj.finance_set.all()
        return FinanceSerializer(finances, many=True).data

    def get_inspections(self, obj):
        inspections = obj.inspections.all()
        return InspectionSerializer(inspections, many=True).data


class ZoneContributiveSerializer(GeoFeatureModelSerializer):
    infrastructures = InfrastructureSerializer(
        many=True, source="infrastructure_set", read_only=True
    )
    infrastructures_count = serializers.IntegerField(
        source="infrastructure_set.count", read_only=True
    )

    class Meta:
        model = ZoneContributive
        # geo_field = "geom"
        fields = "__all__"
        # read_only_fields = ["geom"]


class InspectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inspection
        fields = "__all__"
        depth = 1


class PhotoSerializer(serializers.ModelSerializer):
    related_object = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Photo
        fields = [
            "id",
            "url",
            "description",
            "date_prise",
            "content_type",
            "object_id",
            "related_object",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["content_type", "object_id"]

    def get_related_object(self, obj):
        """
        Returns a dictionary representing the related object.
        """
        if obj.content_object:
            return {
                "type": obj.content_type.model,
                "id": obj.object_id,
                "str": str(obj.content_object),
            }
        return None

    def create(self, validated_data):
        request = self.context["request"]
        model_name = request.data.get("model_name")
        object_id = request.data.get("object_id")

        if not model_name or not object_id:
            raise serializers.ValidationError(
                "`model_name` and `object_id` are required to create a photo."
            )

        # Whitelist allowed models
        ALLOWED = ["infrastructure", "bailleur", "zonecontributive", "inspection"]
        m = model_name.lower()
        if m not in ALLOWED:
            raise serializers.ValidationError(
                f"Model '{model_name}' is not allowed for photo association."
            )

        try:
            ct = ContentType.objects.get(model=m)
        except ContentType.DoesNotExist:
            raise serializers.ValidationError("Invalid model_name.")

        # Validate referenced object exists
        model_class = ct.model_class()
        if not model_class.objects.filter(pk=object_id).exists():
            raise serializers.ValidationError("Referenced object does not exist.")

        validated_data["content_type"] = ct
        validated_data["object_id"] = int(object_id)

        return super().create(validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ShpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shp
        fields = "__all__"
