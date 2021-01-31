from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import RandomIDMixin
from django_lifecycle import BEFORE_CREATE, BEFORE_UPDATE, hook, LifecycleModel

from apps.django.utils.validators import validate_place
from constants import maxlength
from ..public import model_names

if TYPE_CHECKING:
    pass

__all__ = [
    "Room"
]


class Room(RandomIDMixin, LifecycleModel):
    class Meta:
        verbose_name = model_names.ROOM
        verbose_name_plural = model_names.ROOM_PLURAL
        ordering = ("place",)
    
    place = models.CharField(
        verbose_name=_("Ort"),
        max_length=maxlength.ROOM,
        validators=[validate_place],
        unique=True
    )  # type: str
    
    def __str__(self):
        return self.place
    
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
    
    @hook(BEFORE_CREATE)
    @hook(BEFORE_UPDATE, when="place", has_changed=True)
    def _hook_place_validation_and_constraining(self):
        self.place = self.place.upper()
        self.full_clean()
