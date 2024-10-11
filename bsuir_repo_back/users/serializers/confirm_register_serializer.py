from rest_framework import serializers

from users.models import User


class ConfirmRegisterSerializer(serializers.Serializer):
    code = serializers.IntegerField(required=True, )

    def validate(self, attrs):
        code = attrs.get('code')

        if not code:
            raise serializers.ValidationError("Code is required field.")

        if not User.objects.filter(code=code).exists():
            raise serializers.ValidationError("User not found.")

        return attrs
