from django.db import models
from django.utils import timezone


class AuditMixin(models.Model):
    """
    Миксин для отслеживания изменений в модели
    """
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
