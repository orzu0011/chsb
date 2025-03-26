from rest_framework.routers import SimpleRouter
from django.urls import path, include
from users.views import UserViewSet
from rest_framework_simplejwt.views import TokenRefreshView

router = SimpleRouter()
router.register("user", UserViewSet)

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
