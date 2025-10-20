from drf_yasg import openapi
from drf_yasg.app_settings import swagger_settings
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.user.register.serializers import UserRegisterSerializer
from common.utils.generate_token import generate_token_for_user


class UserRegiterAPIView(APIView):
    @swagger_auto_schema(
        request_body=UserRegisterSerializer,
        responses={
            201: openapi.Response('User registered successfully', UserRegisterSerializer),
            400: 'Validation error'
        },
        operation_summary="Register a new user",
        operation_description="Creates a new user account and returns JWT tokens (access, refresh)."
    )
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = generate_token_for_user(user)
            return Response(token, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
