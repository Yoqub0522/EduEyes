from django.urls import path

from api.user.register.views import UserRegiterAPIView

urlpatterns = [
    path('', UserRegiterAPIView.as_view()),
]