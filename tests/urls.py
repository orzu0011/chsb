from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import TestViewSet, TestResultViewSet

router = SimpleRouter()
router.register(r'tests', TestViewSet)
router.register(r'test-results', TestResultViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
