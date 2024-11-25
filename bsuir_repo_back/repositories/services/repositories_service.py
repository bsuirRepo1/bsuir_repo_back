from django.db import transaction
from rest_framework.exceptions import PermissionDenied

from .repository_files_service import RepositoryFilesService
from ..models import Repository
from users.models import User
from common_services.exceptions import UserNotFoundException, RepositoryNotFoundException


class RepositoriesService:
    @staticmethod
    def create_repository(
            user: User, files, name: str, tags: str, description: str = None, archived: bool = False, visible: bool = True
    ):
        try:
            with transaction.atomic():
                files = RepositoryFilesService.save_files_on_google_cloud(file=files)
                files.save()

                repository = Repository.objects.create(
                    user=user,
                    name=name,
                    tags=tags,
                    description=description,
                    archived=archived,
                    visible=visible
                )
                repository.files.add(files)
                repository.save()

                return repository
        except Exception as e:
            raise e

    @staticmethod
    def get_all_repositories():
        return Repository.objects.select_related('user').prefetch_related('files').filter(visible=True, archived=False)

    @staticmethod
    def get_user_repositories(user_id: int):
        if not user_id:
            raise ValueError("User ID is required field.")
        if User.objects.filter(id=user_id).exists():
            repositories = Repository.objects.filter(user=user_id, visible=True, archived=False)
            return repositories
        else:
            raise UserNotFoundException(user_id=user_id)

    @staticmethod
    def get_repository(repository_id: int):
        if not repository_id:
            raise ValueError("Repository ID is required field.")
        try:
            if Repository.objects.filter(id=repository_id, visible=True, archived=False).exists():
                return Repository.objects.get(id=repository_id)
            else:
                raise PermissionDenied("Repository is visible or archived but not found.")
        except RepositoryNotFoundException:
            raise RepositoryNotFoundException(repository_id=repository_id)
