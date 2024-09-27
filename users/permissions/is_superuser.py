from rest_framework.permissions import BasePermission


class IsSuperuser(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return False
