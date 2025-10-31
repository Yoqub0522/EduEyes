from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from math import radians, sin, cos, sqrt, atan2

from apps.Organization.models import Organization, OrganizationImage
from common.serializers.organization.serializers import (
    OrganizationSerializer,
    OrganizationCreateSerializer,
)


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all().select_related("address").prefetch_related("images")
    serializer_class = OrganizationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["org_type"]
    search_fields = ["name"]
    http_method_names = ["get", "post", "patch", "delete"]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return OrganizationCreateSerializer
        return OrganizationSerializer

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('org_type', openapi.IN_QUERY, description="Tashkilot turiga ko‘ra filterlash", type=openapi.TYPE_STRING),
        openapi.Parameter('search', openapi.IN_QUERY, description="Tashkilot nomi bo‘yicha qidirish", type=openapi.TYPE_STRING),
        openapi.Parameter('lat', openapi.IN_QUERY, description="Foydalanuvchining kenglik koordinatasi", type=openapi.TYPE_NUMBER),
        openapi.Parameter('long', openapi.IN_QUERY, description="Foydalanuvchining uzunlik koordinatasi", type=openapi.TYPE_NUMBER),
    ])
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        user_lat = request.query_params.get('lat')
        user_long = request.query_params.get('long')

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

            orgs_with_distance.sort(key=lambda o: (o.distance is None, o.distance))
            serializer = self.get_serializer(orgs_with_distance, many=True)
            data = serializer.data
            for item, org in zip(data, orgs_with_distance):
                item['distance_km'] = round(org.distance, 2) if org.distance else None

            return Response({"message": "Organizations retrieved successfully", "data": data}, status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"message": "Organizations retrieved successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"message": "Organization retrieved successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        organization = serializer.save()
        read_serializer = OrganizationSerializer(organization)
        return Response({"message": "Organization created successfully", "data": read_serializer.data}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        return self._update_instance(request, partial=False)

    def partial_update(self, request, *args, **kwargs):
        return self._update_instance(request, partial=True)

    def _update_instance(self, request, partial):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # Addressni yangilash
        address_data = serializer.validated_data.pop('address', None)
        if address_data:
            for key, value in address_data.items():
                setattr(instance.address, key, value)
            instance.address.save()

        # Rasmlarni yangilash
        images = serializer.validated_data.pop('images', None)
        if images is not None:
            instance.images.all().delete()
            for image in images:
                OrganizationImage.objects.create(organization=instance, image=image)

        # Qolgan maydonlarni yangilash
        for attr, value in serializer.validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        read_serializer = OrganizationSerializer(instance)
        return Response({"message": "Organization updated successfully", "data": read_serializer.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Organization deleted successfully"}, status=status.HTTP_200_OK)

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """Haversine formula orqali masofani km da hisoblaydi"""
        R = 6371
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c
