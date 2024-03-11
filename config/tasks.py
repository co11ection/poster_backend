from django.utils import timezone

from .celery import app
from apps.account.send_email import send_activation_code, send_reset_password


@app.task
def send_email_code_task(to_email, code):
    send_activation_code(to_email, code)


@app.task()
def send_password_reset_email_task(user):
    send_reset_password(user)
