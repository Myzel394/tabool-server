from django_filters.rest_framework import DjangoFilterBackend
from django_hint import RequestType
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.django.main.homework.filters import MaterialFilterSet
from apps.django.main.homework.models import Material
from apps.django.main.homework.serializers import MaterialDetailEndpointSerializer, MaterialListSerializer

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
        return MaterialDetailEndpointSerializer
    
    @action(detail=True, methods=["GET"], url_path="download-link")
    def download_link(self, request: RequestType, pk: str):
        material = get_object_or_404(Material, id=pk)
        
        file = material.file.url or material.get_scooso_download_link(request.user)
        
        if file:
            return Response({
                "file": file
            })
        return Response(status=status.HTTP_502_BAD_GATEWAY)
