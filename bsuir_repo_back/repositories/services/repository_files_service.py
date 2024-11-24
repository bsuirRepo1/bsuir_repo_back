import uuid
import mimetypes
from datetime import datetime

from google.cloud import storage
from django.conf import settings
from google.cloud.exceptions import NotFound
from rest_framework.generics import get_object_or_404

from ..models import RepositoryFile, Repository


class RepositoryFilesService:
    @staticmethod
    def save_files_on_google_cloud(file, expiration_time: int = 3600):
        try:
            storage_client = storage.Client()

            bucket = storage_client.bucket(settings.GS_BUCKET_NAME)

            if hasattr(file, 'file'):
                file_name = file.name
            else:
                file_name = file.split('/')[-1]

            destination_blob_name = f"uploads/{uuid.uuid4()}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{file_name}"
            blob = bucket.blob(destination_blob_name)

            content_type, _ = mimetypes.guess_type(file_name)
            content_type = content_type or 'application/octet-stream'

            if hasattr(file, 'file'):
                blob.upload_from_file(file.file, content_type=content_type)
            else:
                blob.upload_from_file(file, content_type=content_type)

            signed_url = blob.generate_signed_url(expiration_time)

            repository_file = RepositoryFile.objects.create(
                file_name=file_name,
                file_url=signed_url,
                content_type=content_type,
            )

            return repository_file
        except NotFound as nf:
            raise nf
        except Exception as e:
            raise e

    @staticmethod
    def get_repository_files(repository_id: int):
        try:
            repository = get_object_or_404(Repository, id=repository_id)

            files = repository.files.all()

            files_data = [
                {
                    "file_name": file.file_name,
                    "file_url": file.file_url,
                    "content_type": file.content_type,
                }
                for file in files
            ]

            return files_data
        except Exception as e:
            raise e
