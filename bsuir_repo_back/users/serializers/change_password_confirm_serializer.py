from rest_framework import serializers


class ChangePasswordConfirmSerializer(serializers.Serializer):
    code = serializers.IntegerField()

    def validate(self, attrs):
        user = self.context['request'].user

        if user.code != attrs.get('code'):
            raise serializers.ValidationError("Codes are not the same.")

        return attrs
