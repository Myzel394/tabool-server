from rest_framework import permissions

# TODO: Add Email verification
# TODO: Add google login!

__all__ = [
    "AuthenticationAndActivePermission"
]


class AuthenticationAndActivePermission(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_active
