from __future__ import annotations
import random
from django.conf import settings
from django.core.mail import send_mail

from users.models.user import User


class EmailService:
    """
    Functionalities for sending email to users
    Some docs:
    1. All methods are used in our APIs
    --------------------------------------------------------------------------------------------------------------------
    2. If you want to send custom mail - use this method: `send_custom_message`, also don’t forget to look at the
    required parameters for this method to eliminate possible errors
    """
    def generate_code(self) -> int:
        code = random.randint(1000, 9999)

        return code

    def generate_password(self) -> str:
        password = User.objects.make_random_password()

        return password

    def save_code(self, email: str, code: int):
        try:
            user, created = User.objects.get_or_create(email=email)
            user.code = code
            user.save()
        except Exception as e:
            print(e)

    def save_password(self, email: str, password: str):
        user = User.objects.get(email=email)
        try:
            if not user:
                return None
            else:
                user.set_password(password)
                user.save()
        except Exception as e:
            print(e)

    def send_code_to_email(self, email: str):
        code = self.generate_code()
        self.save_code(email, code)

        try:
            send_mail(
                subject="Confirm your email",
                message=f"Your code is {code}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
            )
        except Exception as e:
            print(e)

    def send_password_to_email(self, email: str):
        password = self.generate_password()
        self.save_password(email, password)

        try:
            send_mail(
                subject="Forgot password",
                message=f"Your new password is {password}. You should to change it later",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
            )
        except Exception as e:
            print(e)

    def send_custom_message(self, email: str, subject: str, message: str):
        try:
            send_mail(
                subject,
                message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
            )
        except Exception as e:
            print(e)
