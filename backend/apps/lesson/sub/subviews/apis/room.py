from rest_framework import viewsets

from apps.utils.viewsets.mixins import RetrieveAllMixin
from ....models import Room
from ....serializers import RoomDetailSerializer

__all__ = [
    "RoomViewSet"
]


class RoomViewSet(viewsets.mixins.ListModelMixin, RetrieveAllMixin):
    serializer_class = RoomDetailSerializer
    model = Room
