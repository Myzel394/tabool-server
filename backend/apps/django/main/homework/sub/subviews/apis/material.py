from django_filters.rest_framework import DjangoFilterBackend
from django_hint import RequestType
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from ....filters import MaterialFilterSet
from ....models import Material
from ....serializers import DetailMaterialSerializer, ListMaterialSerializer

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
            return ListMaterialSerializer
        return DetailMaterialSerializer
    
    @action(detail=True, methods=["GET"], url_path="download-link")
    def download_link(self, request: RequestType, pk: str):
        material = get_object_or_404(Material, id=pk)
        
        if material.file.name:
            return Response({
                "file": material.file.url
            })
        
        # Create Scooso link
        url = material.get_scooso_download_link(request.user)
        
        if url:
            return Response({
                "file": url
            })
        return Response(status=status.HTTP_502_BAD_GATEWAY)
