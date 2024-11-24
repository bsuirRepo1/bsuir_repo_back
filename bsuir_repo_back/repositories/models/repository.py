from django.db import models
from django.core.validators import MinLengthValidator

from users.models import User
from common_services.mixins.audit_mixin import AuditMixin


class TagsChoices(models.TextChoices):
    LABS = 'LABS', 'Labs'
    CW = 'CW', 'Control Works'
    TESTS = 'TESTS', 'Tests'
    OTHERS = 'OTHERS', 'Others'


class Repository(AuditMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='repositories')
    files = models.ManyToManyField('RepositoryFile', related_name='repositories')
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
    tags = models.CharField(choices=TagsChoices.choices, default=TagsChoices.OTHERS, max_length=6, null=False)
    archived = models.BooleanField(default=False)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return self.name
