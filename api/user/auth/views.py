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

class CustomRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer