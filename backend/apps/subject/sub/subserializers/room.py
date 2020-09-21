from apps.timetable.models import Room
from apps.utils.serializers import IdMixinSerializer

__all__ = [
    "RoomSerializer"
]


class RoomSerializer(IdMixinSerializer):
    class Meta:
        model = Room
        fields = ["place", "id"]
