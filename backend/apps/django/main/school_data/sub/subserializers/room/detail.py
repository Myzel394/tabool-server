from .base import BaseRoomSerializer

__all__ = [
    "DetailRoomSerializer"
]


class DetailRoomSerializer(BaseRoomSerializer):
    class Meta(BaseRoomSerializer.Meta):
        fields = [
            "place", "id"
        ]
