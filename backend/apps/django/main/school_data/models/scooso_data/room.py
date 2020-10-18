from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.django.utils.models import ScoosoDataMixin
from ...public import *
from ...public import model_names

if TYPE_CHECKING:
    from .. import Room

__all__ = [
    "RoomScoosoData"
]


class RoomScoosoData(ScoosoDataMixin):
    class Meta:
        verbose_name = model_names.ROOM_SCOOSO
        verbose_name_plural = model_names.ROOM_SCOOSO_PLURAL
        ordering = ("code", "scooso_id")
    
    room = models.OneToOneField(
        ROOM,
        on_delete=models.CASCADE,
        verbose_name=model_names.ROOM
    )  # type: Room
    
    code = models.CharField(
        verbose_name=_("Raum-Code"),
        max_length=31,
        blank=True,
        null=True
    )  # type: str
    
    def __str__(self):
        return str(self.room)
