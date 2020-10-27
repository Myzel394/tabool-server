from typing import *

from django_eventstream.channelmanager import DefaultChannelManager
from rest_framework import exceptions, permissions, status, views

if TYPE_CHECKING:
    from apps.django.main.authentication.models import User

__all__ = [
    "AuthenticationAndActivePermission", "unauthorized_handler", "UserActiveChannelManager"
]


def is_user_authorized(user: "User") -> bool:
    return user and \
           user.is_authenticated and \
           user.is_active and \
           user.has_filled_out_data and \
           user.is_confirmed and \
           user.is_scooso_data_valid and \
           not user.is_being_setup


class AuthenticationAndActivePermission(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return is_user_authorized(request.user)


def unauthorized_handler(exc, context):
    response = views.exception_handler(exc, context)
    
    if isinstance(exc, (exceptions.AuthenticationFailed, exceptions.NotAuthenticated)):
        response.status_code = status.HTTP_401_UNAUTHORIZED
    
    return response


class UserActiveChannelManager(DefaultChannelManager):
    def can_read_channel(self, user, _) -> bool:
        return is_user_authorized(user)
