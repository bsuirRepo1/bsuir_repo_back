from rest_framework.response import Response
from rest_framework import status, permissions, parsers, generics
from django.contrib.auth import get_user_model

from users.serializers import RegisterSerializer
from bsuir_repo_core.swagger_service.apply_swagger_auto_schema import apply_swagger_auto_schema


User = get_user_model()


class RegisterView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = RegisterSerializer
    parser_classes = [parsers.MultiPartParser, parsers.JSONParser, ]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


RegisterView = apply_swagger_auto_schema(
    tags=['auth / register'], excluded_methods=[]
)(RegisterView)
