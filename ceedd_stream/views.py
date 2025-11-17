from django.contrib.auth.models import User
from .models import ZoneContributive, Bailleur, TypeInfrastructure, Client, Infrastructure, Finance, Inspection, Photo
from .serializers import UserSerializer, ZoneContributiveSerializer, BailleurSerializer, TypeInfrastructureSerializer, ClientSerializer, InfrastructureSerializer, FinanceSerializer, InspectionSerializer, PhotoSerializer
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.decorators import api_view
from django.db.models import Sum
from datetime import datetime
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Create your views here.
class ZoneContributiveViewSet(viewsets.ModelViewSet):
    queryset = ZoneContributive.objects.prefetch_related('infrastructure_set').all()
    serializer_class = ZoneContributiveSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
    #filterset_fields = ['nom', 'description']
    #search_fields = ['nom', 'description']
    #ordering_fields = ['nom', 'created_at']
    ordering = ['nom']


class BailleurViewSet(viewsets.ModelViewSet):
    queryset = Bailleur.objects.prefetch_related('finances').all()
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
    queryset = Infrastructure.objects.select_related('client', 'type_infrastructure').prefetch_related('finance_set', 'inspections').all()
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


class UserRetrieveView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = 'pk'


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.user
        user_data = UserSerializer(user).data

        tokens = serializer.validated_data

        return Response({
            "refresh": tokens["refresh"],
            "access": tokens["access"],
            "user": user_data
        })


'''On mettra juste une partie de l’adresse (avenue mais pas le numéro, quartier, commune), ceci pourra permettre de faire de requête par quartier, par commune, par avenue.
Par exemple, si on veut connaitre le nombre ou volume des citernes de tel quartier, telle commune ou avenue.
/api/infras/volume?avenue=Mulamba
/api/infras/volume?quartier=Kimbondo
/api/infras/volume?commune=Mont-Ngafula
/api/infras/volume?avenue=Mulamba&quartier=Kimbondo
'''
@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('avenue', openapi.IN_QUERY, required=False, description="Filter by avenue (contains, case-insensitive)", type=openapi.TYPE_STRING),
        openapi.Parameter('quartier', openapi.IN_QUERY, required=False, description="Filter by quartier", type=openapi.TYPE_STRING),
        openapi.Parameter('commune', openapi.IN_QUERY, required=False, description="Filter by commune", type=openapi.TYPE_STRING),
    ],
    responses={
        200: openapi.Response(
            description="Success",
            examples={"application/json": {"total_volume": 1500.50}}
        ),
        404: openapi.Response(
            description="Not Found",
            examples={"application/json": {"message": "No infrastructures found matching the criteria"}}
        )
    }
)
@api_view(http_method_names=['GET'])
def get_volume_by_filters(request):
    avenue = request.query_params.get("avenue")
    quartier = request.query_params.get("quartier")
    commune = request.query_params.get("commune")

    qs = Infrastructure.objects.all()

    if avenue:
        qs = qs.filter(client__avenue__icontains=avenue)

    if quartier:
        qs = qs.filter(client__quartier__icontains=quartier)

    if commune:
        qs = qs.filter(client__commune__icontains=commune)

    if not qs.exists():
        return Response(
            {"message": "No infrastructures found matching the criteria"},
            status=status.HTTP_404_NOT_FOUND,
        )

    total_volume = qs.aggregate(total_volume=Sum('capacite'))['total_volume']

    return Response({"total_volume": total_volume}, status=status.HTTP_200_OK)


'''Pour l’INFRASTRUCTURE on devra plutôt fournir la date de la construction. Le semestre/trimestre/mois/année pourra être obtenu par requête, par exemple,
si on veut connaitre le nombre ou volume des citernes construites au 3 e trimestre 2023
/api/infras/volume_by_date?trimester=3&year=2023
/api/infras/volume_by_date?semester=2
/api/infras/volume_by_date?year=2023
/api/infras/volume_by_date?month=1
/api/infras/volume_by_date?date_from=2023-01-01&date_to=2023-09-30
'''
@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            name='year',
            in_=openapi.IN_QUERY,
            description="Filter by year of construction",
            type=openapi.TYPE_INTEGER
        ),
        openapi.Parameter(
            name='month',
            in_=openapi.IN_QUERY,
            description="Filter by month of construction (1–12)",
            type=openapi.TYPE_INTEGER
        ),
        openapi.Parameter(
            name='trimester',
            in_=openapi.IN_QUERY,
            description="Filter by trimester of construction (1–4)",
            type=openapi.TYPE_INTEGER
        ),
        openapi.Parameter(
            name='semester',
            in_=openapi.IN_QUERY,
            description="Filter by semester of construction (1–2)",
            type=openapi.TYPE_INTEGER
        ),
        openapi.Parameter(
            name='date_from',
            in_=openapi.IN_QUERY,
            description="Start date (YYYY-MM-DD)",
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_DATE
        ),
        openapi.Parameter(
            name='date_to',
            in_=openapi.IN_QUERY,
            description="End date (YYYY-MM-DD)",
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_DATE
        ),
    ],
    responses={
        200: openapi.Response(
            description="Successful response",
            examples={"application/json": {"total_volume": 2500.00}}
        ),
        400: openapi.Response(
            description="Bad Request",
            examples={"application/json": {"error": "trimester must be 1–4"}}
        ),
        404: openapi.Response(
            description="Not Found",
            examples={"application/json": {"message": "No infrastructures found"}}
        ),
    }
)
@api_view(http_method_names=['GET'])
def get_volume_by_date(request):
    qs = Infrastructure.objects.all()

    if not qs.exists():
        return Response(
            {"message": "No infrastructures found"},
            status=status.HTTP_404_NOT_FOUND
        )

    # Extract filters
    year = request.query_params.get("year")
    month = request.query_params.get("month")
    trimester = request.query_params.get("trimester")
    semester = request.query_params.get("semester")
    date_from = request.query_params.get("date_from")
    date_to = request.query_params.get("date_to")

    # --- YEAR ---
    if year:
        qs = qs.filter(date_construction__year=year)

    # --- MONTH ---
    if month:
        qs = qs.filter(date_construction__month=month)

    # --- TRIMESTER ---
    if trimester:
        trimester = int(trimester)
        if trimester not in [1, 2, 3, 4]:
            return Response(
                {"error": "trimester must be 1–4"},
                status=status.HTTP_400_BAD_REQUEST
            )
        month_ranges = {
            1: (1, 3),
            2: (4, 6),
            3: (7, 9),
            4: (10, 12)
        }
        start, end = month_ranges[trimester]
        qs = qs.filter(date_construction__month__gte=start,
                       date_construction__month__lte=end)

    # --- SEMESTER ---
    if semester:
        semester = int(semester)
        if semester not in [1, 2]:
            return Response(
                {"error": "semester must be 1 or 2"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if semester == 1:
            qs = qs.filter(date_construction__month__lte=6)
        else:
            qs = qs.filter(date_construction__month__gte=7)

    # --- Custom date range ---
    if date_from:
        try:
            date_from = datetime.strptime(date_from, "%Y-%m-%d").date()
        except:
            return Response(
                {"error": "date_from must be YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST
            )
        qs = qs.filter(date_construction__gte=date_from)

    if date_to:
        try:
            date_to = datetime.strptime(date_to, "%Y-%m-%d").date()
        except:
            return Response(
                {"error": "date_to must be YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST
            )
        qs = qs.filter(date_construction__lte=date_to)

    # Compute the total volume
    total_volume = qs.aggregate(total_volume=Sum('capacite'))['total_volume']

    return Response(
        {"total_volume": total_volume},
        status=status.HTTP_200_OK
    )
