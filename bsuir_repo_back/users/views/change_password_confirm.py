from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from bsuir_repo_core.swagger_service import apply_swagger_auto_schema
from users.serializers import ChangePasswordConfirmSerializer
from users.permissions import IsBlocked
from users.services.crypt_service import decrypt_password


class ChangePasswordConfirmView(GenericAPIView):
    serializer_class = ChangePasswordConfirmSerializer
    parser_classes = [JSONParser, MultiPartParser]
    permission_classes = [IsAuthenticated, IsBlocked]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            user = request.user
            code = serializer.validated_data['code']
            encrypted_password = request.session.get('encrypted_password')

            if not encrypted_password:
                return Response("No password found. Please initiate the change process again.",
                                status=status.HTTP_400_BAD_REQUEST)

            if user.code == code:
                new_password = decrypt_password(encrypted_password)
                user.set_password(new_password)
                user.code = None
                user.save()

                del request.session['encrypted_password']

                return Response("Password change confirmed", status=status.HTTP_200_OK)
            else:
                return Response("Invalid confirmation code.", status=status.HTTP_400_BAD_REQUEST)


ChangePasswordConfirmView = apply_swagger_auto_schema(
    tags=['change / forgot password'], excluded_methods=[]
)(ChangePasswordConfirmView)
