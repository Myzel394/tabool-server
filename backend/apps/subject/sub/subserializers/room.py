from apps.utils.serializers import IdMixinSerializer
from ...models import Room

__all__ = [
    "RoomSerializer"
]


class RoomSerializer(IdMixinSerializer):
    class Meta:
        model = Room
        fields = ["place", "id"]
