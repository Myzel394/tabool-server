from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import RandomIDMixin

from ...public import *
from ...public import model_verboses

if TYPE_CHECKING:
    from .. import LessonData

__all__ = [
    "LessonDataScoosoData"
]


class LessonDataScoosoData(RandomIDMixin):
    class Meta:
        verbose_name = model_verboses.LESSON_DATA_SCOOSO
        verbose_name_plural = model_verboses.LESSON_DATA_SCOOSO_PLURAL
        ordering = ("lesson_data", "lesson_type")
    
    lesson_data = models.OneToOneField(
        LESSON_DATA,
        on_delete=models.CASCADE,
        verbose_name=model_verboses.LESSON_DATA,
        blank=True,
    )  # type: LessonData
    
    lesson_type = models.UUIDField(
        verbose_name=_("Stundentyp"),
        blank=True,
        null=True
    )  # type: str
    
    def __str__(self):
        return str(self.lesson_data)
