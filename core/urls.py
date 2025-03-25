from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tests.views import (
    ClassViewSet, SubjectViewSet, TestCategoryViewSet, 
    TestViewSet, QuestionViewSet, AnswerViewSet, TestResultViewSet
)
from users.views import UserViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView
)

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
router.register(r'users', UserViewSet, basename='users')
router.register(r'tests', TestViewSet, basename='tests')
router.register(r'user-test-results', TestResultViewSet, basename='test-results')
router.register(r'classes', ClassViewSet, basename='classes')
router.register(r'subjects', SubjectViewSet, basename='subjects')
router.register(r'test-categories', TestCategoryViewSet, basename='test-categories')
router.register(r'questions', QuestionViewSet, basename='questions')
router.register(r'answers', AnswerViewSet, basename='answers')

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin paneli
    path('api/', include(router.urls)),  # API uchun router

    # JWT Token authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Token olish
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Tokenni yangilash
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),  # Tokenni tekshirish

    # Swagger UI va ReDoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
