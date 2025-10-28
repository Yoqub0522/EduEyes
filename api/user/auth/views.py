import random
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenRefreshView

from apps.user.models import User
from common.serializers.user.serializers import (
    UserListSerializer,
    UserRegisterSerializer,
    UserLoginSerializer,
    UserUpdateDetailSerializer,
    UpdateUserSerializer,
    ResetPasswordSerializer,
    SaveResetPasswordSerializer, CustomTokenRefreshSerializer, VerifyCodeSerializer,
)
from config import settings


class UserViewSet(GenericViewSet, RetrieveModelMixin):
    http_method_names = ['get', 'patch', 'post']
    queryset = User.objects.all()
    serializer_class = UserListSerializer

    action_serializers = {
        "register": UserRegisterSerializer,
        "verify_code": VerifyCodeSerializer,
        "update_detail": UserUpdateDetailSerializer,
        "update_me": UpdateUserSerializer,
        "profile": UserListSerializer,
        "reset_password": ResetPasswordSerializer,
        "save_reset_password": SaveResetPasswordSerializer,
        "login": UserLoginSerializer,

    }

    def get_serializer_class(self):
        return self.action_serializers.get(self.action, self.serializer_class)

    def get_permissions(self):
        if self.action in ['update_me', 'profile']:
            return [ IsAuthenticated() ]
        return [AllowAny()]

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='verify-code')
    def verify_code(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.to_representation(user), status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def update_detail(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['patch'], url_path='update-me')
    def update_me(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def profile(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(data=serializer.data)

    @action(detail=False, methods=['post'])
    def reset_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def save_reset_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='resend-or-change-email')
    def resend_or_change_email(self, request):

        username = request.data.get('username')
        new_email = request.data.get('new_email')

        if not username:
            return Response({"detail": "Foydalanuvchi username kiritilishi kerak."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"detail": "Bunday foydalanuvchi topilmadi."},
                            status=status.HTTP_404_NOT_FOUND)

        if user.is_verified:
            return Response({"detail": "Bu foydalanuvchi allaqachon tasdiqlangan."},
                            status=status.HTTP_400_BAD_REQUEST)


        if new_email:
            if User.objects.filter(email=new_email).exists():
                return Response({"detail": "Bu yangi email allaqachon ishlatilgan."},
                                status=status.HTTP_400_BAD_REQUEST)
            user.email = new_email


        code = str(random.randint(100000, 999999))
        user.phone_code = code
        user.code_expires_at = timezone.now() + timezone.timedelta(minutes=5)
        user.save(update_fields=['email', 'phone_code', 'code_expires_at'])


        send_mail(
            subject="Email tasdiqlash kodi",
            message=f"Sizning tasdiqlash kodingiz: {code}\nKod 5 daqiqa davomida amal qiladi.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        return Response({
            "message": "Tasdiqlash kodi emailingizga yuborildi ✅ (5 daqiqa amal qiladi).",
            "email": user.email
        }, status=status.HTTP_200_OK)

class CustomRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer