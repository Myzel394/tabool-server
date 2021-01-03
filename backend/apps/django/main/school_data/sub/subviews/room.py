from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from ...models import Room
from ...paginations import LargeSetPagination
from ...serializers import RoomDetailSerializer

__all__ = [
    "RoomViewSet"
]


class RoomViewSet(viewsets.ModelViewSet):
    filter_backends = [SearchFilter]
    search_fields = ["place"]
    serializer_class = RoomDetailSerializer
    model = Room
    pagination_class = LargeSetPagination
    
    def get_queryset(self):
        if self.action in ["list", "retrieve"]:
            return Room.objects.all()
        return
