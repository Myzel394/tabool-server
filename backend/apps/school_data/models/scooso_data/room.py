from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.utils import ScoosoDataMixin
from ...public import *

__all__ = [
    "RoomScoosoData"
]


class RoomScoosoData(ScoosoDataMixin):
    class Meta:
        verbose_name = _("Raum-Scooso-Daten")
        verbose_name_plural = _("Raum-Scooso-Daten")
        ordering = ("code", "scooso_id")
    
    room = models.OneToOneField(
        ROOM,
        verbose_name=room_single,
        on_delete=models.CASCADE,
        blank=True,
    )
    
    code = models.CharField(
        verbose_name=_("Raum-Code"),
        max_length=31,
        blank=True,
        null=True
    )
