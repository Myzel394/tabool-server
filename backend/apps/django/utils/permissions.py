from typing import *

from django_hint import RequestType
from rest_framework import exceptions, permissions, status, views
from rest_framework.permissions import SAFE_METHODS

if TYPE_CHECKING:
    from apps.django.authentication.user.models import User

__all__ = [
    "AuthenticationAndActivePermission", "unauthorized_handler", "IsTeacher", "IsStudent", "IsTeacherElseReadOnly",
    "IsStudentElseReadOnly"
]


def is_user_authorized(user: "User") -> bool:
    return user and \
           (
                   user.is_authenticated and
                   user.is_active and
                   user.is_confirmed
           ) or user.is_superuser


def unauthorized_handler(exc, context):
    response = views.exception_handler(exc, context)

    if isinstance(exc, (exceptions.AuthenticationFailed, exceptions.NotAuthenticated)):
        response.status_code = status.HTTP_401_UNAUTHORIZED

    return response


class AuthenticationAndActivePermission(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return is_user_authorized(request.user)


class IsTeacher(permissions.BasePermission):
    def has_permission(self, request: RequestType, view):
        return request.user.is_teacher


class IsStudent(permissions.BasePermission):
    def has_permission(self, request: RequestType, view):
        return request.user.is_student


class IsTeacherElseReadOnly(IsTeacher):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return super().has_permission(request, view)


class IsStudentElseReadOnly(IsStudent):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return super().has_permission(request, view)
