from apps.utils.serializers import RandomIDSerializerMixin
from ...models import Room

__all__ = [
    "RoomDetailSerializer"
]


class RoomDetailSerializer(RandomIDSerializerMixin):
    class Meta:
        model = Room
        fields = ["place", "id"]
        read_only_fields = ["id"]
