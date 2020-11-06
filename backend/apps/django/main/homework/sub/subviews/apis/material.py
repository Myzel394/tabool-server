from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from apps.django.main.homework.filters import MaterialFilterSet
from apps.django.main.homework.models import Material
from apps.django.main.homework.serializers import MaterialDetailSerializer, MaterialListSerializer

__all__ = [
    "MaterialViewSet"
]


class MaterialViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = MaterialFilterSet
    search_fields = ["name"]
    ordering_fields = ["added_at", "name"]
    
    def get_queryset(self):
        return Material.objects.user_accessible(self.request.user)
    
    def get_serializer_class(self):
        if self.action == "list":
            return MaterialListSerializer
        return MaterialDetailSerializer
