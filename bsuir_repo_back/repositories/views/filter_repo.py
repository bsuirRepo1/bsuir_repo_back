from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.decorators import action
from rest_framework import permissions, parsers, status

from repositories.serializers import FilterRepoSerializer, RepositorySerializer
from repositories.models import Repository
from users.permissions import IsBlocked


class FilterRepoView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, IsBlocked]
    serializer_class = FilterRepoSerializer
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser]

    @swagger_auto_schema(
        operation_description="Фильтрация репозиториев по факультету, специальности и курсу.",
        tags=["repositories/filter"],
        manual_parameters=[
            openapi.Parameter('faculty', openapi.IN_QUERY,
                              description="Факультет", type=openapi.TYPE_STRING),
            openapi.Parameter('speciality', openapi.IN_QUERY,
                              description="Специальность", type=openapi.TYPE_STRING),
            openapi.Parameter('course', openapi.IN_QUERY,
                              description="Курс", type=openapi.TYPE_STRING),
        ])

    @action(detail=False, methods=['GET'],
            url_path='users/')
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.query_params)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        faculty = request.query_params.get('faculty')
        speciality = request.query_params.get('speciality')
        course = request.query_params.get('course')

        queryset = (Repository.objects.filter(visible=True, archived=False)
                    .only('user', 'name', 'tags'))

        if faculty:
            queryset = queryset.filter(user__userprofile__faculty=faculty)
        if speciality:
            queryset = queryset.filter(user__userprofile__speciality=speciality)
        if course:
            queryset = queryset.filter(user__userprofile__course=course)

        if not queryset.exists():
            return Response({"detail": "Нет репозиториев с такими параметрами."},
                            status=status.HTTP_404_NOT_FOUND)

        serialized_queryset = RepositorySerializer(queryset, many=True)
        return Response(serialized_queryset.data, status=status.HTTP_200_OK)

