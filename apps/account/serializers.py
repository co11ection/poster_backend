from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.core.validators import validate_email
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework.exceptions import ValidationError

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=6,
        max_length=20,
        required=True,
        write_only=True,
        help_text="Пароль должен содержать от 6 до 20 символов.",
    )
    email = serializers.EmailField(required=False)
    phone_number = PhoneNumberField(required=False)
    email_or_phone_number = serializers.CharField(max_length=50, write_only=True)
    
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "phone_number",
            "email_or_phone_number"
        )

    def validate(self, attrs):
        email_or_phone_number = attrs.get("email_or_phone_number")
        if not email_or_phone_number:
            raise serializers.ValidationError("Почта или телефонный номер обязательны")

        if "@" in email_or_phone_number:
            validate_email(email_or_phone_number)
            attrs["email"] = email_or_phone_number
            if User.objects.filter(email=email_or_phone_number).exists():
                raise serializers.ValidationError(
                    "Пользователь с таким email уже существует."
                )
        else:
            attrs["phone_number"] = email_or_phone_number
            if User.objects.filter(phone_number=email_or_phone_number).exists():
                raise serializers.ValidationError(
                    "Пользователь с таким номером телефона уже существует."
                )

        attrs.pop('email_or_phone_number')
        return attrs

    def create(self, validated_data):
        password = validated_data["password"]
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.create_activation_code()
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    email_or_phone_number = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email_or_phone_number = attrs.get("email_or_phone_number")
        password = attrs.get("password")

        user = None
        if "@" in email_or_phone_number:
            user = User.objects.filter(email=email_or_phone_number).first()
        else:
            user = User.objects.filter(phone_number=email_or_phone_number).first()

        if not user or not user.check_password(password):
            raise ValidationError("Неверные учетные данные.")
        
        

        attrs["user"] = user
        return attrs


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100, required=False)
    phone_number = PhoneNumberField(required=False)


class RestorePasswordSerialzer(serializers.Serializer):
    code = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(min_length=6, required=True)
    password2 = serializers.CharField(min_length=6, required=True)

    def validate(self, attrs):
        password2 = attrs.pop("password2")
        if password2 != attrs["password"]:
            raise serializers.ValidationError("password did't match")
        try:
            user = User.objects.get(activation_code=attrs["code"])
        except User.DoesNotExist:
            serializers.ValidationError("Your code is incorrect")
        attrs["user"] = user
        return attrs

    def save(self, **kwargs):
        data = self.validated_data
        user = data["user"]
        user.set_password(data["password"])
        user.activation_code = ""
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password"]


class GetAllUserSerializer(serializers.ModelSerializer):
    average_result = serializers.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "is_active",
            "role",
            "average_result",
        )
