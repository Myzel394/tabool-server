from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from apps.django.authentication.user.constants import STUDENT, TEACHER
from apps.django.utils.permissions import AuthenticationAndActivePermission, IsTeacherElseReadOnly
from apps.django.utils.viewsets import DetailSerializerViewSetMixin
from ....filters import ModificationFilterSet
from ....models import Modification
from ....serializers import (
    CreateModificationSerializer, StudentDetailModificationSerializer, StudentListModificationSerializer,
    TeacherDetailModificationSerializer, TeacherListModificationSerializer, UpdateModificationSerializer,
)

__all__ = [
    "ModificationViewSet"
]


class ModificationViewSet(
    DetailSerializerViewSetMixin,
    viewsets.ModelViewSet
):
    permission_classes = [AuthenticationAndActivePermission & IsTeacherElseReadOnly]
    
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ModificationFilterSet
    search_fields = ["information"]
    
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
