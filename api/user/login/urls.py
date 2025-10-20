from django.urls import path

from api.user.login.views import UserLoginAPIView
from api.user.register.views import UserRegiterAPIView

urlpatterns = [
    path('', UserLoginAPIView.as_view()),
]
