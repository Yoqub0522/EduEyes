from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from apps.Organization.models import Organization
from common.serializers.organization.serializers import OrganizationSerializer, OrganizationCreateSerializer


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return OrganizationCreateSerializer
        return OrganizationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        organization = serializer.save()
        return Response(OrganizationSerializer(organization).data, status=status.HTTP_201_CREATED)
