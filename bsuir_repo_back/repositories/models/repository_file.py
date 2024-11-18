from django.db import models
from google.cloud import storage
from django.conf import settings
from mimetypes import guess_type
import io
import unicodedata
from django.db import transaction

from ..models.repository import Repository
from common_services.mixins.audit_mixin import AuditMixin


class RepositoryFile(AuditMixin):
    CALL_COUNT = 0

    repository = models.ForeignKey(Repository, on_delete=models.CASCADE, related_name='files')
    file_name = models.CharField(max_length=255, null=False)
    file_url = models.URLField(null=False)
    content_type = models.CharField(max_length=50, null=False)

    @classmethod
    def save_multiple_files(cls, repository, files):
        """
        Метод для загрузки нескольких файлов в Google Cloud Storage и сохранения информации в БД
        """
        with transaction.atomic():
            saved_files = []
            for file in files:
                repo_file = cls(repository=repository)
                repo_file.save_file(file)
                saved_files.append(repo_file)
            return saved_files

    def save_file(self, file, file_name="uploaded_file"):
        """
        Загрузка и сохранение файла в Google Cloud
        """
        while self.CALL_COUNT == 0:
            client = storage.Client()
            bucket = client.bucket(settings.GS_BUCKET_NAME)

            file_name = unicodedata.normalize('NFKD', file_name).encode('ascii', 'ignore').decode('ascii')
            blob = bucket.blob(f'uploads/{file_name}')

            file_stream = io.BytesIO(file)
            print("Начало загрузки файла в Google Cloud Storage")
            blob.upload_from_file(file_stream, content_type=guess_type(file_name)[0] or 'application/octet-stream')
            self.CALL_COUNT += 1
            print("Файл успешно загружен в Google Cloud Storage")

            self.content_type = guess_type(file_name)[0] or 'application/octet-stream'
            self.file_name = file_name
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
