from rest_framework import serializers
from apps.Organization.models import Organization, OrganizationImage


class OrganizationImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationImage
        fields = ['id', 'image']


class OrganizationSerializer(serializers.ModelSerializer):
    images = OrganizationImageSerializer(many=True, read_only=True)

    class Meta:
        model = Organization
        fields = ['id', 'name', 'org_type', 'images']


class OrganizationCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True
    )

    class Meta:
        model = Organization
        fields = ['id', 'name', 'org_type', 'images']

    def create(self, validated_data):
        images = validated_data.pop('images', [])
        organization = Organization.objects.create(**validated_data)
        for image in images:
            OrganizationImage.objects.create(organization=organization, image=image)
        return organization
