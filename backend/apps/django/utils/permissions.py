from rest_framework import permissions

__all__ = [
    "AuthenticationAndActivePermission"
]


class AuthenticationAndActivePermission(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_confirmed and request.user.is_active
