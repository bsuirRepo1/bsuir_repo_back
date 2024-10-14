from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.generics import GenericAPIView
from users.serializers import ForgotPassSerializer
from bsuir_repo_core.swagger_service import apply_swagger_auto_schema


class ForgotPasswordView(GenericAPIView):
    serializer_class = ForgotPassSerializer
    parser_classes = [JSONParser, MultiPartParser]
    permission_classes = [AllowAny]

    def post(self, *args, **kwargs):

        if self.request.user:
            return Response({"message": "You are already in system"},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=self.request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "New password has been sent to your email"},
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


ForgotPasswordView = apply_swagger_auto_schema(
    tags=['change / forgot password'], excluded_methods=[]
)(ForgotPasswordView)
