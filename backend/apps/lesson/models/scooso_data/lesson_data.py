from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import RandomIDMixin

from ...public import *

__all__ = [
    "LessonDataScoosoData"
]


class LessonDataScoosoData(RandomIDMixin):
    class Meta:
        verbose_name = _("Stundendaten-Scooso-Daten")
        verbose_name_plural = _("Stundendaten-Scooso-Daten")
        ordering = ("lesson_data", "lesson_type")
    
    lesson_data = models.OneToOneField(
        LESSON_DATA,
        verbose_name=lesson_data_single(),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    
    lesson_type = models.UUIDField(
        verbose_name=_("Stundentyp"),
        blank=True,
        null=True
    )
