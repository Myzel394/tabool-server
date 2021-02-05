from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter

from apps.django.utils.permissions import AuthenticationAndActivePermission, IsTeacherElseReadOnly
from apps.django.utils.viewsets import DetailSerializerViewSetMixin
from ...subfilters.material import MaterialFilterSet
from ....models import Material
from ....serializers import CreateMaterialSerializer, DetailMaterialSerializer, UpdateMaterialSerializer

__all__ = [
    "MaterialViewSet"
]


class MaterialViewSet(
    DetailSerializerViewSetMixin,
    viewsets.ModelViewSet,
):
    permission_classes = [AuthenticationAndActivePermission & IsTeacherElseReadOnly]
    
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = MaterialFilterSet
    ordering_fields = ["created_at", "publish_datetime"]
    
    detail_serializer = DetailMaterialSerializer
    serializer_action_map = {
        "create": CreateMaterialSerializer,
        "update": UpdateMaterialSerializer,
        "partial_update": UpdateMaterialSerializer,
        "retrieve": DetailMaterialSerializer,
        "list": DetailMaterialSerializer
    }
    
    def get_queryset(self):
        return Material.objects.from_user(self.request.user)
