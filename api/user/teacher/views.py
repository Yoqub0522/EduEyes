from rest_framework import viewsets, filters
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from apps.Teacher.models import Teacher
from common.serializers.teacher.serializers import TeacherSerializer, TeacherCreateSerializer


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all().order_by('-created_at')
    serializer_class = TeacherSerializer
    http_method_names = ["get", ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['full_name', 'bio']

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return TeacherCreateSerializer
        return TeacherSerializer

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description="O'qituvchi ismi yoki bio bo'yicha qidirish",
            type=openapi.TYPE_STRING
        )
    ])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
