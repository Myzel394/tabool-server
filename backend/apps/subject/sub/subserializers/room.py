from apps.utils.serializers import IdMixinSerializer
from ...models import Room

__all__ = [
    "RoomDetailSerializer"
]


class RoomDetailSerializer(IdMixinSerializer):
    class Meta:
        model = Room
        fields = ["place", "id"]
