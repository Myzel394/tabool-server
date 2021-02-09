from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from apps.django.authentication.user.constants import STUDENT, TEACHER
from apps.django.utils.permissions import AuthenticationAndActivePermission, IsTeacherElseReadOnly
from apps.django.utils.viewsets import DetailSerializerViewSetMixin
from ...subfilters.material import MaterialFilterSet
from ....models import Material
from ....serializers import (
    CreateMaterialSerializer, StudentDetailMaterialSerializer, TeacherDetailMaterialSerializer,
    UpdateMaterialSerializer,
)

__all__ = [
    "MaterialViewSet"
]


class MaterialViewSet(
    DetailSerializerViewSetMixin,
    viewsets.ModelViewSet,
):
    permission_classes = [AuthenticationAndActivePermission & IsTeacherElseReadOnly]
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = MaterialFilterSet
    ordering_fields = ["created_at", "publish_datetime"]
    search_fields = ["name"]
    
    detail_serializer = {
        STUDENT: StudentDetailMaterialSerializer,
        TEACHER: TeacherDetailMaterialSerializer,
    }
    serializer_action_map = {
        STUDENT: {
            "retrieve": StudentDetailMaterialSerializer,
            "list": StudentDetailMaterialSerializer
        },
        TEACHER: {
            "create": CreateMaterialSerializer,
            "update": UpdateMaterialSerializer,
            "partial_update": UpdateMaterialSerializer,
            "retrieve": TeacherDetailMaterialSerializer,
            "list": TeacherDetailMaterialSerializer
        }
    }
    
    def get_queryset(self):
        return Material.objects.from_user(self.request.user)
