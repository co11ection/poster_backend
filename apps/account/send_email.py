from django.core.mail import send_mail
from decouple import config
from celery import shared_task
from config.settings import EMAIL_HOST_USER


@shared_task()
def send_activation_code(email: str, code: str):
    message = f"Ваш активационный код - {code}"

    send_mail(
        subject="Активация аккаунта",
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=[email],
    )


def send_reset_password(user):
    code = user.activation_code
    to_email = user.email
    send_mail(
        "Subject",
        f"Ваш код для сброса пароля: {code}",
        from_email=EMAIL_HOST_USER[to_email,],
        fail_silently=False,
    )
