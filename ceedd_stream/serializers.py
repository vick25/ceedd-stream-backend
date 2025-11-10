from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import ZoneContributive, Bailleur, TypeInfrastructure, Client, Infrastructure, Finance, Inspection, Photo

class FinanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finance
        fields = '__all__'

class BailleurSerializer(serializers.ModelSerializer):
    finances = FinanceSerializer(many=True, read_only=True)
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

class InfrastructureSerializer(serializers.ModelSerializer):
    #finances = FinanceSerializer(many=True, read_only=True)
    client = ClientSerializer(read_only=True)
    type_infrastructure = TypeInfrastructureSerializer(read_only=True)
    infrastructure_finances = serializers.SerializerMethodField()
    inspections = serializers.SerializerMethodField()
    class Meta:
        model = Infrastructure
        fields = '__all__'

    def get_infrastructure_finances(self, obj):
        # finances = Finance.objects.filter(infrastructure=obj)
        finances = obj.finance_set.all()
        return FinanceSerializer(finances, many=True).data

    def get_inspections(self, obj):
        inspections = obj.inspections.all()
        return InspectionSerializer(inspections, many=True).data

class ZoneContributiveSerializer(GeoFeatureModelSerializer):
    infrastructures = InfrastructureSerializer(many=True, source='infrastructure_set')
    class Meta:
        model = ZoneContributive
        geo_field = "geom"
        fields = '__all__'

class InspectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inspection
        fields = '__all__'

class PhotoSerializer(serializers.ModelSerializer):
    related_object = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Photo
        fields = [
            'id', 'url', 'description', 'date_prise',
            'content_type', 'object_id', 'related_object',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['content_type', 'object_id']

    def get_related_object(self, obj):
        """
        Returns a dictionary representing the related object.
        """
        if obj.content_object:
            return {
                'type': obj.content_type.model,
                'id': obj.object_id,
                'str': str(obj.content_object)
            }
        return None

    def create(self, validated_data):
        model_name = self.context['request'].data.get('model_name')
        object_id = self.context['request'].data.get('object_id')

        if not model_name or not object_id:
            raise serializers.ValidationError("`model_name` and `object_id` are required to create a photo.")

        validated_data['content_type'] = ContentType.objects.get(model=model_name.lower())
        validated_data['object_id'] = object_id
        return super().create(validated_data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user