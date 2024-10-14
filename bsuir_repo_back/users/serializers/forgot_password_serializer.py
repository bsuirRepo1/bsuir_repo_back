from rest_framework import serializers
from users.models import User
from users.tasks import send_password_to_email


class ForgotPassSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        user = User.objects.filter(email=email).first()

        if not user:
            raise serializers.ValidationError("No user with such email")

        if user.code:
            raise serializers.ValidationError("Try to confirm your email before this action")

        return attrs

    def save(self, **kwargs):
        email = self.validated_data['email']
        send_password_to_email.delay(email=email)
