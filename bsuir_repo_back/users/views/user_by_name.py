from rest_framework.response import Response
from rest_framework import status, permissions, parsers
from rest_framework.generics import GenericAPIView
from rest_framework.decorators import action

from users.models import User
from users.serializers import UserSerializer
from bsuir_repo_core.swagger_service import apply_swagger_auto_schema
from users.permissions import IsBlocked


class UserByNameView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, IsBlocked]
    serializer_class = UserSerializer
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser]

    @action(detail=True, methods=['GET'], url_path='users/(?P<username>[^/]+)')
    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')

        user = (User.objects.filter(username=username)
                .select_related('userprofile')
                .only('id', 'username', 'email', 'date_joined')
                .first())

        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serialized_user = UserSerializer(user)
        return Response(serialized_user.data)


UserByNameView = apply_swagger_auto_schema(
    tags=['users'], excluded_methods=[]
)(UserByNameView)
