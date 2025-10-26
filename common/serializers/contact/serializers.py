from rest_framework import serializers

from apps.contact.models import Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            "id",
            "gmail",
            "fullname",
            "message",

        ]


class ContactCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            "id",
            "gmail",
            "fullname",
            "message",

        ]

    def create(self, validated_data):
        contact = Contact.objects.create(**validated_data)
        return contact