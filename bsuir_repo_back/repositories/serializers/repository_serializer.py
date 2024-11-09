from rest_framework import serializers

from ..models.repository_file import RepositoryFile
from ..models.repository import Repository


class RepositoryFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepositoryFile
        fields = ['file_name', 'file_url', 'content_type']


class RepositorySerializer(serializers.ModelSerializer):
    files = serializers.ListField(child=serializers.FileField(allow_empty_file=False), write_only=True)

    class Meta:
        model = Repository
        fields = ['name', 'description', 'tags', 'files']

    def create(self, validated_data):
        files = validated_data.pop('files')
        repository = Repository.create_repository_with_files(
            user=self.context['request'].user,
            name=validated_data['name'],
            description=validated_data['description'],
            tags=validated_data['tags'],
            files=files
        )

        return repository
