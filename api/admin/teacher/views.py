from rest_framework import status, viewsets
from rest_framework.response import Response

from apps.Teacher.models import Teacher
from common.serializers.teacher.serializers import TeacherSerializer, TeacherCreateSerializer


class TeacherViewSet(viewsets.ModelViewSet):

    queryset = Teacher.objects.all().order_by('-created_at')
    serializer_class = TeacherSerializer
    http_method_names = ["get", "post", "patch", "delete"]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return TeacherCreateSerializer
        return TeacherSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        teacher = serializer.save()
        return Response(
            TeacherSerializer(teacher).data,
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        teacher = self.get_object()
        serializer = self.get_serializer(teacher, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            TeacherSerializer(teacher).data,
            status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        teacher = self.get_object()
        teacher.delete()
        return Response(
            {"detail": "Teacher successfully deleted."},
            status=status.HTTP_204_NO_CONTENT
        )
