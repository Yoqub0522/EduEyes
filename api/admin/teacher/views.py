from rest_framework import status, viewsets, filters
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from apps.Teacher.models import Teacher
from common.serializers.teacher.serializers import TeacherSerializer, TeacherCreateSerializer


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all().order_by('-created_at')
    serializer_class = TeacherSerializer
    http_method_names = ["get", "post", "patch", "delete"]
    filter_backends = [filters.SearchFilter]
    search_fields = ['full_name', 'bio']

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return TeacherCreateSerializer
        return TeacherSerializer

    # --- SWAGGER PARAMETRLAR ---
    search_param = openapi.Parameter(
        name="search",
        in_=openapi.IN_QUERY,
        description="O'qituvchi ismi yoki bio bo'yicha qidirish",
        type=openapi.TYPE_STRING,
    )
    organization_param = openapi.Parameter(
        name="organization",
        in_=openapi.IN_QUERY,
        description="Tashkilot nomi bo‘yicha o‘qituvchilarni filtrlash",
        type=openapi.TYPE_STRING,
    )

    # --- SWAGGER: list uchun to‘liq response bilan ---
    @swagger_auto_schema(
        manual_parameters=[search_param, organization_param],
        responses={
            200: openapi.Response(
                description="O‘qituvchilar ro‘yxati",
                schema=TeacherSerializer(many=True)
            )
        }
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        organization_name = request.query_params.get('organization')
        if organization_name:
            queryset = queryset.filter(organization__name__icontains=organization_name)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=TeacherCreateSerializer,
        responses={201: openapi.Response("Yaratildi", TeacherSerializer())},
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        teacher = serializer.save()
        return Response(TeacherSerializer(teacher).data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=TeacherCreateSerializer,
        responses={200: openapi.Response("Yangilandi", TeacherSerializer())},
    )
    def update(self, request, *args, **kwargs):
        teacher = self.get_object()
        serializer = self.get_serializer(teacher, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(TeacherSerializer(teacher).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={204: openapi.Response(description="O‘chirildi")}
    )
    def destroy(self, request, *args, **kwargs):
        teacher = self.get_object()
        teacher.delete()
        return Response(
            {"detail": "O'qituvchi muvaffaqiyatli o'chirildi."},
            status=status.HTTP_204_NO_CONTENT
        )
