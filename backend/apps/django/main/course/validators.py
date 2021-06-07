from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from .models import Room

__all__ = [
    "does_room_exist"
]


def does_room_exist(value: str) -> None:
    available_room_ids = set(Room.objects.all().values_list("id", flat=True))

    if value in available_room_ids:
        raise ValidationError(_('This field must be unique.'))
