from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema

from ..serializers.repository_serializer import RepositoryCreateSerializer, RepositorySerializer
from users.permissions.is_blocked import IsBlocked
from bsuir_repo_core.swagger_service.apply_swagger_auto_schema import apply_swagger_auto_schema
from ..services.repositories_service import RepositoriesService

rep_service = RepositoriesService()


class RepositoryViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated, IsBlocked]

    def get_serializer_class(self):
        if hasattr(self.request, 'method'):
            match self.request.method:
                case 'GET':
                    return RepositorySerializer
                case 'POST':
                    return RepositoryCreateSerializer

    def get_queryset(self):
        data = rep_service.get_all_repositories()

        return data

    def retrieve(self, request, *args, **kwargs):
        repositories = rep_service.get_repository(repository_id=kwargs['pk'])
        data = RepositorySerializer(repositories).data

        return Response(data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return serializer.data

    @action(detail=False, methods=['GET'], url_path='user-repository/(?P<user_id>[^/.]+)')
    def get_user_repositories(self, request, user_id: int):
        repositories = rep_service.get_user_repositories(user_id=user_id)
        return Response(RepositorySerializer(repositories, many=True).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(auto_schema=None)
    def update(self, request, *args, **kwargs):
        return Response("Method not allowed", status.HTTP_405_METHOD_NOT_ALLOWED)


RepositoryViewSet = apply_swagger_auto_schema(
    tags=['repositories'], excluded_methods=[]
)(RepositoryViewSet)
