from rest_framework import serializers
from apps.Teacher.models import Teacher


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = [
            "id",
            "username",
            "full_name",
            "bio",
            "phone",
            "rating",
            "image",
            "organization",
        ]


class TeacherCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = [
            "id",
            "username",
            "full_name",
            "bio",
            "phone",
            "rating",
            "image",
            "organization",
        ]

    def create(self, validated_data):
        teacher = Teacher.objects.create(**validated_data)
        return teacher
