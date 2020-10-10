from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from apps.homework.models import Material
from apps.homework.sub.subfilters import MaterialFilterSet
from apps.homework.sub.subserializers import MaterialDetailSerializer, MaterialListSerializer

__all__ = [
    "MaterialViewSet"
]


class MaterialViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = MaterialFilterSet
    search_fields = ["name"]
    ordering_fields = ["added_at"]
    
    def get_queryset(self):
        return Material.objects.user_accessible(self.request.user)
    
    def get_serializer_class(self):
        if self.action == "list":
            return MaterialListSerializer
        return MaterialDetailSerializer
