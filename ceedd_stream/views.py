from django.shortcuts import render
from .models import ZoneContributive, Bailleur, TypeInfrastructure, Client, Infrastructure, Finance, Inspection, Photo
from .serializers import ZoneContributiveSerializer
from rest_framework import viewsets


# Create your views here.
class ZoneContributiveViewSet(viewsets.ModelViewSet):
    queryset = ZoneContributive.objects.all()
    serializer_class = ZoneContributiveSerializer
    #filterset_fields = ['nom', 'description']
    #search_fields = ['nom', 'description']
    #ordering_fields = ['nom', 'created_at']
    ordering = ['nom']