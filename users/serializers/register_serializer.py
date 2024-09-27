from rest_framework import serializers

from users.models.user import User
from users.services.email_service import EmailService
from users.models.profile import UserProfile


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)
    password_confirm = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password_confirm')

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError("Passwords mismatch.")

        if User.objects.filter(email=attrs.get('email'), username=attrs.get('username')).exists():
            raise serializers.ValidationError("Email already registered.")

        if User.objects.filter(email=attrs.get('email'), username=attrs.get('username'), code__isnull=False).exists():
            raise serializers.ValidationError(
                "The user has completed the first stage of registration,"
                " confirm the code sent to your email."
            )

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data.get('email'),
            username=validated_data.get('username'),
            password=validated_data.get('password'),
        )

        sender_service = EmailService()

        sender_service.send_code_to_email(email=user.email)

        # TODO: Фиксануть скорость работы апишки ( нет двухфакторки на мыло и из-за этого долго приходит ответ )

        UserProfile.objects.create(user=user)

        return user
