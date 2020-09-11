from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models import RandomIDMixin
from django_common_utils.libraries.utils import model_verbose
from django_hint import *
from django_lifecycle import BEFORE_CREATE, BEFORE_UPDATE, hook, LifecycleModel

from apps.utils.validators import validate_place
from constants import maxlength
from .. import constants

if TYPE_CHECKING:
    from .. import Lesson


class Room(RandomIDMixin, LifecycleModel):
    class Meta:
        verbose_name = _("Raum")
        verbose_name_plural = _("Räume")
        ordering = ("place",)
        app_label = constants.APP_LABEL
    
    place = models.CharField(
        verbose_name=_("Ort"),
        max_length=maxlength.ROOM
    )  # type: str
    
    def __str__(self):
        return f"{model_verbose(self.__class__)}: {self.place}"
    
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
    
    @hook(BEFORE_CREATE)
    @hook(BEFORE_UPDATE, when="place")
    def _hook_place_validation_and_constraining(self):
        self.place = self.place.capitalize()
        validate_place(self.place)
    
    @property
    def lessons(self) -> QueryType["Lesson"]:
        return self.lesson_set.all()
