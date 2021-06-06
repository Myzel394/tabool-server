from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import RandomIDMixin
from django_hint import *

from ..public import model_names
from ..sub.subquerysets.timetable import TimetableQuerySet

if TYPE_CHECKING:
    from . import Lesson

__all__ = [
    "Timetable"
]


class Timetable(RandomIDMixin):
    class Meta:
        verbose_name = model_names.TIMETABLE
        verbose_name_plural = model_names.TIMETABLE_PLURAL
        ordering = ("name",)

    objects = TimetableQuerySet.as_manager()

    start_date = models.DateField(
        verbose_name=_("Beginn des Schuljahres"),
    )

    end_date = models.DateField(
        verbose_name=_("Ende des Schuljahres")
    )

    name = models.CharField(
        verbose_name=_("Bezeichnung"),
        max_length=31,
        unique=True,
    )

    @property
    def lessons(self) -> QueryType["Lesson"]:
        return self.lesson_set.all()
