from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.crypto import get_random_string
from .managers import UserManagers
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractBaseUser):
    ROLE_CHOICES = (
        ("user", "Пользователь"),
        ("admin", "Администратор"),
        ("owner", "Владелец"),
    )
    username = models.CharField(verbose_name="Никнейм", max_length=50)
    email = models.EmailField(
        verbose_name="Электронная почта", blank=True, null=True, unique=True
    )
    phone_number = PhoneNumberField(verbose_name="Телефон", max_length=23)
    photo = models.ImageField(
        upload_to="upload/", verbose_name="Фотография", blank=True, null=True
    )
    phone_number = models.CharField(
        max_length=30, verbose_name="Номер телефона", blank=True, null=True, unique=True
    )
    is_active = models.BooleanField(default=False, verbose_name="Активен")
    is_staff = models.BooleanField(default=False, verbose_name="Персонал")
    is_admin = models.BooleanField(default=False, verbose_name="Администратор")
    activation_code = models.CharField(
        max_length=8, blank=True, verbose_name="Код активации"
    )
    role = models.CharField(
        default="user", choices=ROLE_CHOICES, max_length=12, verbose_name="Роль"
    )

    objects = UserManagers()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone_number", "username"]

    def create_activation_code(self):
        code = get_random_string(length=8)
        self.activation_code = code
        self.save()

    def __str__(self) -> str:
        return f"{self.email}"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
