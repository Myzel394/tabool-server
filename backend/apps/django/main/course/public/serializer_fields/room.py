from apps.django.utils.serializers import WritableAllFieldMixin
from ...models import Room

__all__ = [
    "RoomField"
]


class RoomField(WritableAllFieldMixin):
    model = Room
