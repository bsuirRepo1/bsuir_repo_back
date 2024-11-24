from rest_framework import serializers

from ..models.repository_file import RepositoryFile


class RepositoryFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepositoryFile
        fields = ['file_name', 'file_url', 'content_type']
