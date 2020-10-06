from django.contrib.auth.models import Permission
from rest_framework import permissions

# TODO: Add Email verification

__all__ = [
    "AuthenticationAndActivePermission"
]


class AuthenticationAndActivePermission(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_email_verified


def perm_to_permission(identifier: str) -> Permission:
    app_label, codename = identifier.split(".")
    
    return Permission.objects.get(
        content_type__app_label=app_label,
        codename=codename
    )
