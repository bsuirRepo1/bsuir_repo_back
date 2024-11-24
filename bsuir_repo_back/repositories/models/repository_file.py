from django.db import models

from common_services.mixins.audit_mixin import AuditMixin


class RepositoryFile(AuditMixin):
    file_name = models.CharField(max_length=255, null=False)
    file_url = models.URLField(null=False, max_length=2048)
    content_type = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.file_name
