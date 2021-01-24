from apps.django.utils.serializers import WritableAllFieldMixin
from ...models import Room
from ...sub.subserializers.room.detail import DetailRoomSerializer

__all__ = [
    "RoomField"
]


class RoomField(WritableAllFieldMixin):
    model = Room
    detail_serializer = DetailRoomSerializer
