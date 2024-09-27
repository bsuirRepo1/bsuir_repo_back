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
    def user_by_name(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = kwargs.get('username')

        try:
            user = (User.objects.filter(username=username)
                    .select_related('userprofile')
                    .only('id', 'username', 'email', 'date_joined'))

            return Response(UserSerializer(user).data)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


UserByNameView = apply_swagger_auto_schema(
    tags=['users'], excluded_methods=[]
)(UserByNameView)
