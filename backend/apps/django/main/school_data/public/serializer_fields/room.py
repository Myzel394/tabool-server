from apps.django.main.school_data.models import Room
from apps.django.main.school_data.sub.subserializers.room import RoomDetailSerializer
from apps.django.utils.serializers import WritableAllFieldMixin

__all__ = [
    "RoomField"
]


class RoomField(WritableAllFieldMixin):
    model = Room
    detail_serializer = RoomDetailSerializer
