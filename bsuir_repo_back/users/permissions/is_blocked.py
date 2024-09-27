from rest_framework.permissions import BasePermission


class IsBlocked(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_blocked:
            return False
        return True
