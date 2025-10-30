from django.contrib.auth.models import User
from .models import ZoneContributive, Bailleur, TypeInfrastructure, Client, Infrastructure, Finance, Inspection, Photo
from .serializers import UserSerializer, ZoneContributiveSerializer, BailleurSerializer, TypeInfrastructureSerializer, ClientSerializer, InfrastructureSerializer, FinanceSerializer, InspectionSerializer, PhotoSerializer
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly


# Create your views here.
class ZoneContributiveViewSet(viewsets.ModelViewSet):
    queryset = ZoneContributive.objects.all()
    serializer_class = ZoneContributiveSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
    #filterset_fields = ['nom', 'description']
    #search_fields = ['nom', 'description']
    #ordering_fields = ['nom', 'created_at']
    ordering = ['nom']


class BailleurViewSet(viewsets.ModelViewSet):
    queryset = Bailleur.objects.all()
    serializer_class = BailleurSerializer
    lookup_field = 'pk'

class TypeInfrastructureViewSet(viewsets.ModelViewSet):
    queryset = TypeInfrastructure.objects.all()
    serializer_class = TypeInfrastructureSerializer
    lookup_field = 'pk'

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    lookup_field = 'pk'

class FinanceViewSet(viewsets.ModelViewSet):
    queryset = Finance.objects.all()
    serializer_class = FinanceSerializer
    lookup_field = 'pk'

class InfrastructureViewSet(viewsets.ModelViewSet):
    queryset = Infrastructure.objects.all()
    serializer_class = InfrastructureSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'pk'

class InspectionViewSet(viewsets.ModelViewSet):
    queryset = Inspection.objects.all()
    serializer_class = InspectionSerializer
    lookup_field = 'pk'

class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    lookup_field = 'pk'

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]