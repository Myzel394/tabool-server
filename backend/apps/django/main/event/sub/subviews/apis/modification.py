from rest_framework import viewsets

from apps.django.main.event.models import Modification
from apps.django.main.event.serializers import (
    CreateModificationSerializer, DetailModificationSerializer, ListModificationSerializer,
    UpdateModificationSerializer,
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
    detail_serializer = DetailModificationSerializer
    serializer_action_map = {
        "create": CreateModificationSerializer,
        "update": UpdateModificationSerializer,
        "partial_update": UpdateModificationSerializer,
        "detail": DetailModificationSerializer,
        "list": ListModificationSerializer,
    }
    
    def get_queryset(self):
        return Modification.ordering.from_user(self.request.user)
