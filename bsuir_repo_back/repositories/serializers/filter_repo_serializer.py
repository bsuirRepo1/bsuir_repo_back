from rest_framework import serializers
from users.models.profile import FacultyChoices, SpecialitiesChoices, CourseChoices


class FilterRepoSerializer(serializers.Serializer):
    faculty = serializers.ChoiceField(choices=FacultyChoices.choices, required=False)
    speciality = serializers.ChoiceField(choices=SpecialitiesChoices.choices, required=False)
    course = serializers.ChoiceField(choices=CourseChoices.choices, required=False)

    def validate(self, data):
        # Может быть проверка на соответсвие факультета и специальности

        # faculty = data.get('faculty')
        # specialty = data.get('specialty')
        # course = data.get('course')

        return data
