from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import RandomIDMixin

from ...public import *
from ...public import model_names

if TYPE_CHECKING:
    from .. import Lesson

__all__ = [
    "LessonScoosoData"
]


class LessonScoosoData(RandomIDMixin):
    class Meta:
        verbose_name = model_names.LESSON_SCOOSO
        verbose_name_plural = model_names.LESSON_SCOOSO_PLURAL
        ordering = ("lesson", "time_id")
    
    lesson = models.OneToOneField(
        LESSON,
        on_delete=models.CASCADE,
        verbose_name=model_names.LESSON,
        blank=True,
    )  # type: Lesson
    
    time_id = models.PositiveSmallIntegerField(
        verbose_name=_("Time-ID"),
        blank=True,
        null=True
    )  # type: int
    
    lesson_type = models.UUIDField(
        verbose_name=_("Stundentyp"),
        blank=True,
        null=True
    )  # type: str
    
    def __str__(self):
        return str(self.lesson)
