from rest_framework import serializers
from apps.user.models import User
from common.utils.generate_token import generate_token_for_user
from messages.get_message import get_message


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    tokens = serializers.DictField(read_only=True)
    message = serializers.CharField(read_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError(get_message("1005"))

        if not user.check_password(password):
            raise serializers.ValidationError(get_message("1005"))

        token = generate_token_for_user(user)
        attrs['tokens'] = token
        attrs['message'] = get_message("1006")
        return attrs
