from django.contrib.auth.models import Permission
from rest_framework import permissions

__all__ = [
    "AuthenticationAndActivePermission"
]


class AuthenticationAndActivePermission(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_confirmed


def perm_to_permission(identifier: str) -> Permission:
    app_label, codename = identifier.split(".")
    
    return Permission.objects.get(
        content_type__app_label=app_label,
        codename=codename
    )
