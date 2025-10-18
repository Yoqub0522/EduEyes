from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi




# --- Admin API Swagger ---
admin_schema_view = get_schema_view(
    openapi.Info(
        title="EduEyes Admin API",
        default_version='v1',
        description="Swagger documentation for Admin API endpoints.",
        contact=openapi.Contact(email="axmedov.yoqub0522@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    patterns=[
        path('api/admins/', include('api.admin.urls')),
    ]
)

# --- User API Swagger ---
# user_schema_view = get_schema_view(
#     openapi.Info(
#         title="EduEyes User API",
#         default_version='v1',
#         description="Swagger documentation for User API endpoints.",
#         contact=openapi.Contact(email="axmedov.yoqub0522@gmail.com"),
#         license=openapi.License(name="BSD License"),
#     ),
#     public=True,
#     patterns=[
#         path('api/users/', include('api.user.urls')),
#     ]
# )


urlpatterns = [

    path('admin/', admin.site.urls),

    # --- API routes ---
    path('api/admins/', include('api.admin.urls')),
    # path('api/users/', include('api.user.urls')),

    # --- Swagger Docs ---
    path('swagger/admins/', admin_schema_view.with_ui('swagger', cache_timeout=0), name='admins-swagger-ui'),
    # path('swagger/users/', user_schema_view.with_ui('swagger', cache_timeout=0), name='users-swagger-ui'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
