from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tests.views import (
    TestViewSet, UserTestResultViewSet
)
from users.views import UserViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger uchun schema view
schema_view = get_schema_view(
    openapi.Info(
        title="Test Tizimi API",
        default_version='v1',
        description="Test tizimi uchun avtomatik generatsiya qilingan API hujjatlar",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="admin@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
)

# DefaultRouter
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'tests', TestViewSet)
router.register(r'user-test-results', UserTestResultViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin paneli
    path('api/', include(router.urls)),  # API uchun router

    # Swagger UI va ReDoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
