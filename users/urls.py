from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig
from users.views import (PaymentCreateAPIView, PaymentsListAPIView,
                         UserCreateAPIView, UserDestroyAPIView,
                         UserListAPIView, UserPaymentsListAPIView,
                         UserRetreiveAPIView, UserUpdateAPIView)

app_name = UsersConfig.name


urlpatterns = [
    path("user/create/", UserCreateAPIView.as_view(), name="user_create"),
    path("users/", UserListAPIView.as_view(), name="user_list"),
    path("user/<int:pk>/", UserRetreiveAPIView.as_view(), name="user_detail"),
    path("user/update/<int:pk>/", UserUpdateAPIView.as_view(), name="user_update"),
    path("user/delete/<int:pk>/", UserDestroyAPIView.as_view(), name="user_delete"),
    # Payment endpoints
    path("payments/", PaymentsListAPIView.as_view(), name="payments_list"),
    path(
        "user_payments/", UserPaymentsListAPIView.as_view(), name="user_payments_list"
    ),
    path("payments/create/", PaymentCreateAPIView.as_view(), name="payment_create"),
    # Getting tokens endpoints
    path(
        "user/login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
]
