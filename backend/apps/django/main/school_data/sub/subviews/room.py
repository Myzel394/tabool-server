from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from apps.django.utils.viewsets import RetrieveAllMixin
from ...models import Room
from ...paginations import LargeSetPagination
from ...serializers import RoomDetailSerializer

__all__ = [
    "RoomViewSet"
]


class RoomViewSet(viewsets.mixins.ListModelMixin, RetrieveAllMixin):
    filter_backends = [SearchFilter]
    search_fields = ["place"]
    serializer_class = RoomDetailSerializer
    model = Room
    pagination_class = LargeSetPagination
