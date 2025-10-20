from drf_yasg import openapi
from drf_yasg.app_settings import swagger_settings
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.user.login.serializers import UserLoginSerializer
from api.user.register.serializers import UserRegisterSerializer

class UserLoginAPIView(APIView):
    @swagger_auto_schema(
        request_body=UserLoginSerializer,
        responses={
            201: openapi.Response('User registered successfully', UserRegisterSerializer),
            400: 'Validation error'
        },
        operation_summary="Register a new user",
        operation_description="Creates a new user account and returns JWT tokens (access, refresh)."
    )
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        return Response(data, status=status.HTTP_200_OK)
