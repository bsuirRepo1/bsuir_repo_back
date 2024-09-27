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

    def save_code(self, email: str, code: int):
        user = User.objects.get(email=email)
        try:
            if not user:
                return None
            else:
                user.code = code
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
