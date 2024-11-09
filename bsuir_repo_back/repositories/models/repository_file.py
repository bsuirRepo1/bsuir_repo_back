from django.db import models
from google.cloud import storage
from django.conf import settings
from mimetypes import guess_type

from ..models.repository import Repository
from common_services.mixins.audit_mixin import AuditMixin


class RepositoryFile(AuditMixin):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE, related_name='repository_files')
    file_name = models.CharField(max_length=255, null=False)
    file_url = models.URLField(null=False)
    content_type = models.CharField(max_length=50, null=False)

    @classmethod
    def save_multiple_files(cls, repository, files):
        """
        Метод для загрузки нескольких файлов в Google Cloud Storage и сохранения информации в БД
        """
        saved_files = []
        for file in files:
            repo_file = cls(repository=repository)
            repo_file.save_file(file)
            saved_files.append(repo_file)
        return saved_files

    def save_file(self, file):
        """
        Загрузка и сохранение файла в Google Cloud
        """
        client = storage.Client()
        bucket = client.bucket(settings.GS_BUCKET_NAME)

        blob = bucket.blob(f'uploads/{file.name}')
        blob.upload_from_file(file)

        self.content_type = guess_type(file.name)[0] or 'application/octet-stream'

        self.file_name = file.name
        self.file_url = blob.public_url
        self.save()

    def get_file_content(self):
        """
        Метод для получения содержимого файла
        """
        client = storage.Client()
        bucket = client.bucket(settings.GS_BUCKET_NAME)
        blob = bucket.blob(f'uploads/{self.file_name}')
        content = blob.download_as_text()

        return content

    def __str__(self):
        return self.file_name
