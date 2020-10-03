from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import RandomIDMixin

from ...public import *

__all__ = [
    "LessonScoosoData"
]


class LessonScoosoData(RandomIDMixin):
    class Meta:
        verbose_name = _("Stunde-Scooso-Daten")
        verbose_name_plural = _("Stunden-Scooso-Daten")
        ordering = ("lesson", "time_id")
    
    lesson = models.OneToOneField(
        LESSON,
        verbose_name=lesson_single,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    
    time_id = models.PositiveSmallIntegerField(
        verbose_name=_("Time-ID"),
        blank=True,
        null=True
    )
