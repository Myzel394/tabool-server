from rest_framework import exceptions, permissions, status, views

__all__ = [
    "AuthenticationAndActivePermission", "unauthorized_handler"
]


class AuthenticationAndActivePermission(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        # Authenticated
        if request.user and request.user.is_authenticated:
            return request.user.is_confirmed and request.user.is_active


def unauthorized_handler(exc, context):
    response = views.exception_handler(exc, context)
    
    if isinstance(exc, (exceptions.AuthenticationFailed, exceptions.NotAuthenticated)):
        response.status_code = status.HTTP_401_UNAUTHORIZED
    
    return response
