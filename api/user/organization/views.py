from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from math import radians, sin, cos, sqrt, atan2

from apps.Organization.models import Organization
from common.serializers.organization.serializers import (
    OrganizationSerializer,
    OrganizationCreateSerializer,
)


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all().select_related("address")
    serializer_class = OrganizationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["org_type"]
    search_fields = ["name"]
    http_method_names = ["get"]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return OrganizationCreateSerializer
        return OrganizationSerializer

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            'org_type',
            openapi.IN_QUERY,
            description="Tashkilot turiga ko‘ra filterlash. Mumkin bo‘lgan qiymatlar: 'university', 'school', 'private_school'",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description="Tashkilot nomi bo‘yicha qidirish",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'lat',
            openapi.IN_QUERY,
            description="Foydalanuvchining kenglik (latitude) koordinatasi",
            type=openapi.TYPE_NUMBER
        ),
        openapi.Parameter(
            'long',
            openapi.IN_QUERY,
            description="Foydalanuvchining uzunlik (longitude) koordinatasi",
            type=openapi.TYPE_NUMBER
        ),
    ])
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        user_lat = request.query_params.get('lat')
        user_long = request.query_params.get('long')

        # Agar foydalanuvchi joylashuvi berilgan bo‘lsa:
        if user_lat and user_long:
            user_lat = float(user_lat)
            user_long = float(user_long)

            orgs_with_distance = []
            for org in queryset:
                if org.address and org.address.lat and org.address.long:
                    dist = self.calculate_distance(user_lat, user_long, org.address.lat, org.address.long)
                else:
                    dist = None
                org.distance = dist
                orgs_with_distance.append(org)

            # Masofa bo‘yicha sortlash
            orgs_with_distance.sort(key=lambda o: (o.distance is None, o.distance))
            serializer = self.get_serializer(orgs_with_distance, many=True)
            data = serializer.data

            # distance maydonini qo‘shamiz (km)
            for item, org in zip(data, orgs_with_distance):
                item['distance_km'] = round(org.distance, 2) if org.distance else None

            return Response(data, status=status.HTTP_200_OK)

        return super().list(request, *args, **kwargs)

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """Haversine formulasi orqali ikki nuqta orasidagi masofani km da hisoblaydi."""
        R = 6371  # Yer radiusi (km)
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c
        return distance
