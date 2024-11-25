from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

from .user_exception import UserNotFoundException


def custom_exception_handler(exc, context):
    if isinstance(exc, UserNotFoundException):
        return Response(
            {"detail": exc.message},
            status=status.HTTP_404_NOT_FOUND,
        )

    response = exception_handler(exc, context)

    return response
