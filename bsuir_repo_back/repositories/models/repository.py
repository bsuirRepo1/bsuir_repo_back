from django.db import models
from django.core.validators import MinLengthValidator
from django.core.exceptions import ObjectDoesNotExist

from users.models import User
from common_services.mixins.audit_mixin import AuditMixin


class TagsChoices(models.TextChoices):
    LABS = 'LABS', 'Labs'
    CW = 'CW', 'Control Works'
    TESTS = 'TESTS', 'Tests'
    OTHERS = 'OTHERS', 'Others'


class Repository(AuditMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='repositories')
    name = models.CharField(
        max_length=70,
        validators=[MinLengthValidator(3)],
        unique=True,
        null=False,
        error_messages={
            'unique': "A repository with this name already exists.",
            'min_length': "A repository with this name must have at least 3 characters.",
            'max_length': "A repository with this name must have at most 70 characters.",
            'null': "This field is required.",
        }
    )
    description = models.TextField(null=False)
    tags = models.CharField(choices=TagsChoices, default=TagsChoices.OTHERS, max_length=6, null=False)
    archived = models.BooleanField(default=False)
    visible = models.BooleanField(default=True)

    def get_user_all_repositories(self, user_id: int):
        """
        Метод для получения всепх репозиториев конкретного пользователя
        """
        repositories = Repository.objects.filter(user_id=user_id)

        return repositories

    def get_specific_user_repository(self, user_id: int, repository_id: int):
        """
        Метод для получения конкретного репозитория пользователя
        """
        repository = Repository.objects.filter(user_id=user_id, pk=repository_id).first()

        return repository

    def get_specific_repository(self, repository_id: int):
        try:
            repository = Repository.objects.filter(id=repository_id).first()
            if repository and not repository.archived and repository.visible:
                return repository
            else:
                raise ValueError(f"Repository with id {repository_id} does not exist or archived.")
        except Exception as e:
            return ValueError(f"Something went wrong: {str(e)}")

    def get_all_user_archive_repositories(self, user_id: int):
        """
        Метод для получения всех репозиториев конкретного пользователя, которые попали в архив
        """
        user_exists = User.objects.filter(id=user_id).exists()
        if user_exists:
            repositories = Repository.objects.filter(user_id=user_id, archived=True)
            return repositories
        else:
            raise ValueError(f"User with id {user_id} does not exist.")

    def get_specific_user_archive_repository(self, user_id: int, repository_id: int):
        try:
            # user = User.objects.filter(pk=user_id).first().exists()
            repository = Repository.objects.filter(user_id=user_id, id=repository_id).first()
            return repository
        except ObjectDoesNotExist:
            raise ValueError(f"User with id {user_id} does not exist.")
        except ObjectDoesNotExist:
            raise ValueError(f"Repository with id {repository_id} does not exist.")
