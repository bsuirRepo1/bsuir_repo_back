from rest_framework import serializers

from users.models import UserProfile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class ProfilePatchSerializer(serializers.Serializer):
    photo = serializers.ImageField(required=False)
    about = serializers.CharField(required=False, max_length=1000)
    city = serializers.CharField(required=False, max_length=30)

    def validate(self, attrs):
        if not any([attrs.get('about'), attrs.get('city'), attrs.get('photo')]):
            raise serializers.ValidationError("At least one field must be provided.")

        return attrs

    def update(self, instance, validated_data):
        instance.photo = validated_data.get('photo', instance.photo)
        instance.city = validated_data.get('city', instance.city)
        instance.about = validated_data.get('about', instance.about)
        instance.save()

        return instance
