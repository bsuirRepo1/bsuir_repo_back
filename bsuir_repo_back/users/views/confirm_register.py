from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework import status

from bsuir_repo_core.swagger_service.apply_swagger_auto_schema import apply_swagger_auto_schema
from users.serializers.confirm_register_serializer import ConfirmRegisterSerializer
from users.models import User


class ConfirmRegisterView(GenericAPIView):
    serializer_class = ConfirmRegisterSerializer
    permission_classes = [AllowAny, ]
    parser_classes = [MultiPartParser, JSONParser]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.data['code']
        user = User.objects.filter(code=code).first()

        if user.code == code:
            user.code = None
            user.is_active = True
            user.save()

            return Response("Successfully!", status=status.HTTP_200_OK)
        else:
            return Response("Code doesn't match!", status=status.HTTP_400_BAD_REQUEST)


ConfirmRegisterView = apply_swagger_auto_schema(
    tags=['auth / register'], excluded_methods=[]
)(ConfirmRegisterView)
