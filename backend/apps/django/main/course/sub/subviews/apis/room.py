from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from apps.django.utils.viewsets import DetailSerializerViewSetMixin
from ....models import Room
from ....serializers import CreateRoomSerializer, DetailRoomSerializer

__all__ = [
    "RoomViewSet"
]


class RoomViewSet(
    DetailSerializerViewSetMixin,
    viewsets.mixins.CreateModelMixin,
    viewsets.mixins.RetrieveModelMixin,
    viewsets.mixins.ListModelMixin,
):
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["place"]
    ordering_fields = ["place", "-place"]
    model = Room
    detail_serializer = DetailRoomSerializer
    serializer_action_map = {
        "create": CreateRoomSerializer,
        "retrieve": DetailRoomSerializer,
        "list": DetailRoomSerializer
    }

    def get_queryset(self):
        return Room.objects.all()
