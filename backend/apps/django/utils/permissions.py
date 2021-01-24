from typing import *

from rest_framework import exceptions, permissions, status, views

if TYPE_CHECKING:
    from apps.django.main.authentication.models import User

__all__ = [
    "AuthenticationAndActivePermission", "unauthorized_handler",
]


class AuthenticationAndActivePermission(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return is_user_authorized(request.user)


def is_user_authorized(user: "User") -> bool:
    return user and \
           (
                   user.is_authenticated and
                   user.is_active and
                   user.has_filled_out_data and
                   user.is_confirmed and
                   user.is_scooso_data_valid
           ) or user.is_superuser


def unauthorized_handler(exc, context):
    response = views.exception_handler(exc, context)
    
    if isinstance(exc, (exceptions.AuthenticationFailed, exceptions.NotAuthenticated)):
        response.status_code = status.HTTP_401_UNAUTHORIZED
    
    return response
