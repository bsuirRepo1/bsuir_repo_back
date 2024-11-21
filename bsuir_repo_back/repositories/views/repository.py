from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated

from ..serializers.repository_serializer import RepositorySerializer, RepositoryCreateSerializer
from users.permissions.is_blocked import IsBlocked
from ..models.repository import Repository
from bsuir_repo_core.swagger_service.apply_swagger_auto_schema import apply_swagger_auto_schema


class RepositoryViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated, IsBlocked]
    serializer_class = RepositorySerializer

    def get_serializer_class(self):
        if hasattr(self.request, 'method'):
            match self.request.method:
                case 'GET':
                    return RepositorySerializer
                case 'POST':
                    return RepositoryCreateSerializer

    def get_queryset(self):
        user = self.request.user
        data = Repository.get_user_all_repositories(user_id=user.pk)

        return data

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


RepositoryViewSet = apply_swagger_auto_schema(
    tags=['repositories'], excluded_methods=[]
)(RepositoryViewSet)
