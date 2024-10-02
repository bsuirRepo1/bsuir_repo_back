from rest_framework import serializers
from django.contrib.auth.hashers import check_password


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, min_length=8)
    new_password = serializers.CharField(required=True, min_length=8)
    new_password_confirm = serializers.CharField(required=True, min_length=8)

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        new_password_confirm = attrs.get('new_password_confirm')
        user = self.context['request'].user

        if not check_password(old_password, user.password):
            raise serializers.ValidationError("Your old password does not match. If you forgot it, go to recovery.")

        if new_password != new_password_confirm:
            raise serializers.ValidationError("Your new password does not match.")

        if new_password == old_password:
            raise serializers.ValidationError("Your new password does not match.")

        return attrs
