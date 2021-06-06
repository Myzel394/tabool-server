from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import RandomIDMixin

from ..public import model_names

__all__ = [
    "Room"
]


class Room(RandomIDMixin):
    class Meta:
        verbose_name = model_names.ROOM
        verbose_name_plural = model_names.ROOM_PLURAL
        ordering = ("place",)

    place = models.CharField(
        verbose_name=_("Ort"),
        max_length=15,
        unique=True
    )  # type: str

    def __str__(self):
        return self.place
