from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated

from ..serializers.repository_serializer import RepositoryCreateSerializer, RepositorySerializer
from users.permissions.is_blocked import IsBlocked
from bsuir_repo_core.swagger_service.apply_swagger_auto_schema import apply_swagger_auto_schema
from ..services.repositories_service import RepositoriesService


class RepositoryViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated, IsBlocked]
    serializer_class = RepositoryCreateSerializer

    def get_serializer_class(self):
        if hasattr(self.request, 'method'):
            match self.request.method:
                case 'GET':
                    return RepositorySerializer
                case 'POST':
                    return RepositoryCreateSerializer

    def get_queryset(self):
        user = self.request.user
        data = RepositoriesService.get_all_user_repositories(user_id=user.pk)

        return data

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return serializer.data


RepositoryViewSet = apply_swagger_auto_schema(
    tags=['repositories'], excluded_methods=[]
)(RepositoryViewSet)
