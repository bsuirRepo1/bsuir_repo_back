from rest_framework import serializers

from users.models import User
from users.models import UserProfile
from users.serializers import ProfileSerializer


class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined', 'profile']
        read_only_fields = ['date_joined', 'profile']

    def get_profile(self, obj):
        profile = UserProfile.objects.filter(user=obj).first()
        data = ProfileSerializer(profile).data

        return data


class UserPatchSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False, max_length=25)

    def validate(self, attrs):
        email = attrs.get('email')
        username = attrs.get('username')

        if not email and not username:
            raise serializers.ValidationError("All fields are required.")

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email address is already in use.")

        return attrs

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.save()

        return instance
