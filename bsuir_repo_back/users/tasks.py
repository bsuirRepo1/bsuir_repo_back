from celery import shared_task
from .services import EmailService

sender_service = EmailService()


@shared_task()
def send_code_to_email(email: str):
    sender_service.send_code_to_email(email=email)  # отправка письма с помощью EmailService


@shared_task()
def send_password_to_email(email: str):
    sender_service.send_password_to_email(email=email)
