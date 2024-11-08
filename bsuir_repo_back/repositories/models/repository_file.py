from django.db import models

from .repository import Repository
from common_services.mixins.audit_mixin import AuditMixin


class RepositoryFile(AuditMixin):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE, related_name='repository_files')
    file_name = models.CharField(max_length=255, null=False)
    file_url = models.URLField(null=False)
    content_type = models.CharField(max_length=50, null=False)

    def save_file(self, file): pass

    def get_file_content(self): pass

    def __str__(self):
        return self.file_name
