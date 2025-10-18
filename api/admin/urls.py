from django.urls import path,include


urlpatterns=[
    path('organization/',include('api.admin.organization.urls')),
    path('teacher/',include('api.admin.teacher.urls')),
]