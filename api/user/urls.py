from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('login/', include('api.user.login.urls')),
    path('organization/', include('api.user.organization.urls')),
    path('teacher/', include('api.user.teacher.urls')),
    path('register/', include('api.user.register.urls')),
]
