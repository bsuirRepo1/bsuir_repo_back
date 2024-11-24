from rest_framework import serializers

from ..models.repository import Repository
from ..services import RepositoriesService, RepositoryFilesService


class RepositorySerializer(serializers.ModelSerializer):
    files = serializers.SerializerMethodField()

    class Meta:
        model = Repository
        fields = ['id', 'name', 'tags', 'description', 'archived', 'visible', 'files']

    def get_files(self, obj):
        obj = RepositoryFilesService.get_repository_files(repository_id=obj.id)
        return obj


class RepositoryCreateSerializer(serializers.ModelSerializer):
    files = serializers.FileField(allow_empty_file=False, write_only=True)

    class Meta:
        model = Repository
        fields = ['name', 'tags', 'description', 'archived', 'visible', 'files']

    def create(self, validated_data):
        files = validated_data.pop('files')
        repository = RepositoriesService.create_repository(
            user=self.context['request'].user,
            name=validated_data['name'],
            tags=validated_data['tags'],
            description=validated_data['description'],
            archived=validated_data['archived'],
            visible=validated_data['visible'],
            files=files
        )

        return repository
