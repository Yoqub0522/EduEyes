from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from apps.Organization.models import Organization
from common.serializers.organization.serializers import OrganizationSerializer, OrganizationCreateSerializer


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['org_type']
    search_fields = ['name']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return OrganizationCreateSerializer
        return OrganizationSerializer

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            'org_type',
            openapi.IN_QUERY,
            description="Tashkilot turiga ko'ra filterlash. Mumkin bo'lgan qiymatlar: 'university', 'school', 'private_school'",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description="Tashkilot nomiga ko'ra qidirish",
            type=openapi.TYPE_STRING
        )
    ])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        organization = serializer.save()
        return Response(OrganizationSerializer(organization).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        organization = serializer.save()
        return Response(OrganizationSerializer(organization).data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
