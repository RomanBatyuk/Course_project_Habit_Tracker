from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# from rest_framework.routers import SimpleRouter
from users.apps import UsersConfig

app_name = UsersConfig.name

# router = SimpleRouter()
# router.register("payments", PaymentViewSet)

urlpatterns = [
    path(
        "token/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="token_obtain_pair",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    # path("register/", CustomUserCreateAPIView.as_view(), name="register"),
]
