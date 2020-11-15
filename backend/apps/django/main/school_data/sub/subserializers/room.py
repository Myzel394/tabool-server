from apps.django.utils.serializers import PreferredIdsMixin, RandomIDSerializerMixin
from ...models import Room

__all__ = [
    "RoomDetailSerializer"
]


class RoomDetailSerializer(RandomIDSerializerMixin, PreferredIdsMixin):
    preferred_id_key = "room"
    
    class Meta:
        model = Room
        fields = ["place", "id"]
