from rest_framework import viewsets, status, permissions, parsers
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from bsuir_repo_core.swagger_service import apply_swagger_auto_schema
from users.models import UserProfile
from users.permissions import IsBlocked
from users.serializers.profile_serializer import ProfilePatchSerializer, ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser]
    permissions = [permissions.IsAuthenticated, IsBlocked]

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return ProfilePatchSerializer
        return ProfileSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            users = UserProfile.objects.all()

            return users

        if not user.is_superuser:
            profile = UserProfile.objects.filter(user=user)

            return profile

    @swagger_auto_schema(auto_schema=None)
    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @swagger_auto_schema(auto_schema=None)
    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @swagger_auto_schema(auto_schema=None)
    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data

        serializer = ProfilePatchSerializer(instance=instance, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


ProfileViewSet = apply_swagger_auto_schema(
    tags=['profile'], excluded_methods=[]
)(ProfileViewSet)
