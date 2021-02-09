from rest_framework import viewsets

from apps.django.authentication.user.constants import STUDENT, TEACHER
from apps.django.main.event.models import Modification
from apps.django.main.event.serializers import (
    CreateModificationSerializer, StudentDetailModificationSerializer, StudentListModificationSerializer,
    TeacherDetailModificationSerializer, TeacherListModificationSerializer, UpdateModificationSerializer,
)
from apps.django.utils.permissions import AuthenticationAndActivePermission, IsTeacherElseReadOnly
from apps.django.utils.viewsets import DetailSerializerViewSetMixin

__all__ = [
    "ModificationViewSet"
]


class ModificationViewSet(
    DetailSerializerViewSetMixin,
    viewsets.ModelViewSet
):
    permission_classes = [AuthenticationAndActivePermission & IsTeacherElseReadOnly]
    detail_serializer = {
        STUDENT: StudentDetailModificationSerializer,
        TEACHER: TeacherDetailModificationSerializer
    }
    serializer_action_map = {
        STUDENT: {
            "detail": StudentDetailModificationSerializer,
            "list": StudentListModificationSerializer,
        },
        TEACHER: {
            "create": CreateModificationSerializer,
            "update": UpdateModificationSerializer,
            "partial_update": UpdateModificationSerializer,
            "detail": TeacherDetailModificationSerializer,
            "list": TeacherListModificationSerializer,
        },
    }
    
    def get_queryset(self):
        return Modification.objects.from_user(self.request.user)
