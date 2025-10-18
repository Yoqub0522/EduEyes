from rest_framework.routers import DefaultRouter
from .views import TeacherViewSet

router = DefaultRouter()
router.register(r'teachers', TeacherViewSet, basename='teachers')

urlpatterns = router.urls
