from django.urls import path
from rest_framework.routers import DefaultRouter

from api.user.auth.views import UserViewSet, CustomRefreshView

router = DefaultRouter()
router.register('', UserViewSet, basename='user')

urlpatterns = [

path('refresh-token/', CustomRefreshView.as_view(), name='refresh_token')

]+router.urls