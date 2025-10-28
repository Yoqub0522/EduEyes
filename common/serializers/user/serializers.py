from rest_framework import serializers
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import random
from apps.user.models import User
from common.utils.generate_token import generate_token_for_user
from rest_framework_simplejwt.serializers import TokenRefreshSerializer



class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'phone_number',
            'birth_date', 'role', 'is_verified'
        ]


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password', 'username', 'phone_number']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Bu email allaqachon ro‘yxatdan o‘tgan.")
        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Parollar mos emas."})
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('confirm_password')

        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.is_verified = False
        user.is_active = False
        user.save()

        # 🔹 6 xonali kod
        code = str(random.randint(100000, 999999))
        user.phone_code = code
        user.code_expires_at = timezone.now() + timedelta(minutes=5)
        user.save(update_fields=['phone_code', 'code_expires_at'])

        # 🔹 Emailga yuborish
        send_mail(
            subject="Tasdiqlash kodi",
            message=f"Sizning tasdiqlash kodingiz: {code}\nKod 5 daqiqa davomida amal qiladi.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return user

    def to_representation(self, instance):
        return {
            "message": "Ro‘yxatdan o‘tish muvaffaqiyatli ✅ Tasdiqlash kodi emailingizga yuborildi (5 daqiqa amal qiladi).",
            "user": UserListSerializer(instance).data
        }



class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "Bunday foydalanuvchi topilmadi."})

        if user.phone_code != data['code']:
            raise serializers.ValidationError({"code": "Tasdiqlash kodi noto‘g‘ri."})

        if not user.code_expires_at or timezone.now() > user.code_expires_at:
            raise serializers.ValidationError({"code": "Kod muddati tugagan. Iltimos, yangisini oling."})

        # foydalanuvchini validatsiyadan o‘tkazdik
        data['user'] = user
        return data

    def save(self, **kwargs):
        user = self.validated_data['user']
        user.is_verified = True
        user.is_active = True
        user.phone_code = None
        user.code_expires_at = None
        user.save()
        return user  # << shu joy MUHIM: dict emas, model obyekt qaytadi

    def to_representation(self, instance):
        """ instance bu user obyekt """
        tokens = generate_token_for_user(instance)
        return {
            "message": "Foydalanuvchi muvaffaqiyatli tasdiqlandi ✅",
            "tokens": tokens,
            "user": UserListSerializer(instance).data
        }



class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data.get('email'), password=data.get('password'))
        if not user:
            raise serializers.ValidationError("Email yoki parol noto‘g‘ri.")
        if not user.is_verified:
            raise serializers.ValidationError("Email hali tasdiqlanmagan.")
        self.user = user
        return data

    def to_representation(self, instance):
        tokens = generate_token_for_user(self.user)
        return {
            "message": "Kirish muvaffaqiyatli amalga oshirildi ✅",
            "tokens": tokens,
            "user": UserListSerializer(self.user).data
        }



class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Bu email bilan foydalanuvchi topilmadi.")

        code = str(random.randint(100000, 999999))
        user.phone_code = code
        user.code_expires_at = timezone.now() + timedelta(minutes=5)
        user.save(update_fields=['phone_code', 'code_expires_at'])

        send_mail(
            subject="Parolni tiklash kodi",
            message=f"Sizning parolni tiklash kodingiz: {code}\nKod 5 daqiqa davomida amal qiladi.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[data['email']],
            fail_silently=False,
        )
        return {"email": data['email']}

    def to_representation(self, instance):
        return {
            "message": "Parolni tiklash uchun kod emailingizga yuborildi (5 daqiqa amal qiladi)."
        }



class SaveResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True, min_length=6)

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError({"detail": "Bunday foydalanuvchi topilmadi."})

        if user.phone_code != data['code']:
            raise serializers.ValidationError({"code": "Kod noto‘g‘ri."})
        if not user.code_expires_at or timezone.now() > user.code_expires_at:
            raise serializers.ValidationError({"code": "Kod muddati tugagan. Iltimos, yangisini oling."})

        data['user'] = user
        return data

    def save(self, **kwargs):
        user = self.validated_data['user']
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.phone_code = None
        user.code_expires_at = None
        user.save()
        return user

    def to_representation(self, instance):
        return {
            "message": "Parol muvaffaqiyatli o‘zgartirildi ✅",
            "user": UserListSerializer(instance).data
        }



class UserUpdateDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'birth_date', 'role', 'is_verified']


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'phone_number', 'birth_date']


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.token_class(attrs['refresh'])
        user = User.objects.get(id=refresh['user_id'])
        data['user'] = UserListSerializer(user).data
        return data
