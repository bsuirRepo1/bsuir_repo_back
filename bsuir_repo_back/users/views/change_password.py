from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from users.serializers import ChangePasswordSerializer
from bsuir_repo_core.swagger_service import apply_swagger_auto_schema
from users.permissions.is_blocked import IsBlocked
from users.services.crypt_service import encrypt_password
from users.tasks import send_code_to_email


class ChangePasswordView(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    parser_classes = [JSONParser, MultiPartParser]
    permission_classes = [IsAuthenticated, IsBlocked]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            user = request.user

            new_password = serializer.validated_data['new_password']
            encrypted_password = encrypt_password(new_password)
            request.session['encrypted_password'] = encrypted_password

            send_code_to_email.delay(email=user.email)

            return Response("Confirm your action. Code has been send to email!", status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


ChangePasswordView = apply_swagger_auto_schema(
    tags=['change / forgot password'], excluded_methods=[]
)(ChangePasswordView)
