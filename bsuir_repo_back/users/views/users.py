from rest_framework import viewsets, status, permissions, parsers
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from users.models import User
from users.permissions import IsBlocked
from bsuir_repo_core.swagger_service.apply_swagger_auto_schema import apply_swagger_auto_schema
from users.serializers import UserSerializer, UserPatchSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsBlocked]
    serializer_class = UserSerializer
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser]

    def get_queryset(self):
        if self.request.user.is_superuser:
            users = User.objects.all().select_related('profile')

            return users
        if not self.request.user.is_superuser:
            users = (User.objects.all()
                     .select_related('userprofile')
                     .exclude(is_blocked=True, is_superuser=True, is_active=False)
                     .only('id', 'username', 'email', 'date_joined'))

            return users

        return User.objects.none()

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

        serializer = UserPatchSerializer(data, instance, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


UserViewSet = apply_swagger_auto_schema(
    tags=['users'], excluded_methods=[]
)(UserViewSet)
