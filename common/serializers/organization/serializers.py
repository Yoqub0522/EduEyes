from rest_framework import serializers
from apps.Organization.models import Organization, OrganizationImage
from apps.addres.models import Address


# 🏠 Address (manzil) serializer
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'street_name', 'lat', 'long']


# 🖼️ OrganizationImage serializer
class OrganizationImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationImage
        fields = ['id', 'image']


# 🏢 Organization serializer (GET uchun)
class OrganizationSerializer(serializers.ModelSerializer):
    images = OrganizationImageSerializer(many=True, read_only=True)
    address = AddressSerializer(read_only=True)
    org_type = serializers.ChoiceField(
        choices=Organization._meta.get_field('org_type').choices,
        help_text="Tashkilot turi (University, School, Private School)"
    )
    distance = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Organization
        fields = ['id', 'name', 'org_type', 'address', 'images', 'distance']

    def get_distance(self, obj):
        """Masofani km da qaytaradi (ViewSetda hisoblanadi)"""
        return getattr(obj, 'distance', None)


# 🏗️ Organization yaratish uchun serializer (POST uchun)
class OrganizationCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False  # <-- required=False qo'shing
    )
    address = AddressSerializer(write_only=True)
    org_type = serializers.ChoiceField(
        choices=Organization._meta.get_field('org_type').choices,
        help_text="Tashkilot turi (University, School, Private School)"
    )

    class Meta:
        model = Organization
        fields = ['id', 'name', 'org_type', 'address', 'images']

    def create(self, validated_data):
        images = validated_data.pop('images', [])  # <-- default bo'sh list
        address_data = validated_data.pop('address')

        # Avval addressni yaratamiz
        address = Address.objects.create(**address_data)

        # Keyin organizationni address bilan yaratamiz
        organization = Organization.objects.create(address=address, **validated_data)

        # Rasmlarni qo'shamiz (agar mavjud bo'lsa)
        for image in images:
            OrganizationImage.objects.create(organization=organization, image=image)

        return organization
