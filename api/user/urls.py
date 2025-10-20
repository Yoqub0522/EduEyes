from django.urls import path,include


urlpatterns=[
    path('organization/',include('api.user.organization.urls')),
    path('teacher/',include('api.user.teacher.urls')),
    path('register/',include('api.user.register.urls')),
]