from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.http import HttpResponse
from config.tasks import send_email_code_task, send_password_reset_email_task

from .serializers import (
    RegistrationSerializer,
    UserLoginSerializer,
    ForgotPasswordSerializer,
    RestorePasswordSerialzer,
    UserProfileSerializer,
    GetAllUserSerializer,
)

User = get_user_model()


class RegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user.email:
                try:
                    send_email_code_task.delay(user.email, user.activation_code)
                except:
                    return Response(
                        {
                            "msg": "Зарегистрировано, но возникла проблема с отправкой подтверждения",
                            "data": serializer.data,
                        },
                        status=status.HTTP_201_CREATED,
                    )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivationView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ""
            user.save()
            html_content = render_to_string("users/activation_success.html")
            return HttpResponse(html_content)
        except User.DoesNotExist:
            html_content = render_to_string("users/activation_error.html")
            return HttpResponse(html_content, status=status.HTTP_404_NOT_FOUND)


class UserLoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(
            data=request.data, context={"request": request}
        )
        
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            
            if not user.is_active:
                return Response('Нет активных пользователей по этим учетным данным')
            
            refresh = RefreshToken.for_user(user)
            return Response(
                {"refresh": str(refresh), "access": str(refresh.access_token)},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get("email")
        phone_number = serializer.data.get("phone_number")
        if email:
            try:
                user = User.objects.get(email=email)
                user.create_ativation_code()
                user.save()
                send_password_reset_email_task.delay(user)
                return Response("check your mail", status=200)
            except User.DoesNotExist:
                return Response("User with this email  does not exist", status=404)
        elif phone_number:
            try:
                user = User.objects.get(phone_number=phone_number)
                user.create_ativation_code()
                user.save()
                return Response("check your sms", status=200)
            except:
                return Response(
                    "User with this phone_number does not exist", status=404
                )


class RestorePasswordView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = RestorePasswordSerialzer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("Password changed successfully", status=200)
