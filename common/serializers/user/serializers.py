from rest_framework import serializers
from apps.user.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class UserListSerializer(serializers.ModelSerializer):
    """Foydalanuvchilar ro‘yxati uchun"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'role', 'is_verified']


class UserDetailSerializer(serializers.ModelSerializer):
    """Bitta foydalanuvchi ma’lumotlari uchun"""
    class Meta:
        model = User
        fields = '__all__'


class UserCreateSerializer(serializers.ModelSerializer):
    """Yangi foydalanuvchi ro‘yxatdan o‘tkazish uchun"""
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone_number', 'role']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Foydalanuvchi ma’lumotlarini yangilash uchun"""
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'birth_date', 'is_verified', 'role']


class UserLoginSerializer(serializers.Serializer):
    """Login uchun serializer (JWT token qaytaradi)"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Email yoki parol noto‘g‘ri")

        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
            }
        }
