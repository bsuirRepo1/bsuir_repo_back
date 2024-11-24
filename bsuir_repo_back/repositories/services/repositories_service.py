from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from .repository_files_service import RepositoryFilesService
from ..models import Repository
from users.models import User


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
    def get_all_user_repositories(user_id: int):
        if not user_id:
            raise ValueError("User ID is required field.")
        if User.objects.filter(id=user_id).exists():
            repositories = Repository.objects.filter(user=user_id)
            return repositories
        else:
            raise ObjectDoesNotExist("User does not exist.")
