from rest_framework import serializers

from apps.user.models import User
from messages.get_message import get_message


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name',
                  'last_name',
                  'username',
                  'phone_number',
                  'email',
                  'password']

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        user = User.objects.filter(username=username).exists()
        user2 = User.objects.filter(email=email).exists()
        if user:
            raise serializers.ValidationError(get_message("1003"))
        if user2:
            raise serializers.ValidationError(get_message("1004"))
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
