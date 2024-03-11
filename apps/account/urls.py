from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter

from .views import (
    RegistrationView,
    UserLoginAPIView,
    ActivationView,
    ForgotPasswordView,
    RestorePasswordView,
)


urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register"),
    path("activate/<str:activation_code>/", ActivationView.as_view(), name="activate"),
    path("login/", UserLoginAPIView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("forgot_password/", ForgotPasswordView.as_view(), name="forgot_password"),
    path("restore_password", RestorePasswordView.as_view(), name="restore_password"),
]
