from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from apps.user.models import User
from common.serializers.user.serializers import (
    UserListSerializer, UserDetailSerializer,
    UserCreateSerializer, UserUpdateSerializer,
    UserLoginSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_permissions(self):
        if self.action in ['create', 'login']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return UserUpdateSerializer
        elif self.action == 'retrieve':
            return UserDetailSerializer
        elif self.action == 'login':
            return UserLoginSerializer
        return UserListSerializer

    @action(detail=False, methods=['post'])
    def login(self, request):
        """Login va JWT token olish"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
