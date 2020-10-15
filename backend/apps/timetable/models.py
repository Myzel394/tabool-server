from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import CustomQuerySetMixin, RandomIDMixin
from django_lifecycle import BEFORE_CREATE, BEFORE_UPDATE, hook, LifecycleModel

from apps.lesson.public import model_references, model_verbose_functions
from apps.timetable.sub.subquerysets import TimetableQuerySet
from apps.timetable.utils import create_designation_from_date
from apps.timetable.validators import validate_lessons_dont_overlap
from apps.utils import AssociatedUserMixin
from constants import maxlength

__all__ = [
    "Timetable"
]


class Timetable(
    RandomIDMixin,
    AssociatedUserMixin,
    
    LifecycleModel,
    CustomQuerySetMixin,
):
    class Meta:
        verbose_name = _("Stundenplan")
        verbose_name_plural = _("Stundenpläne")
        ordering = ("designation",)
    
    objects = TimetableQuerySet.as_manager()
    
    lessons_data = models.ManyToManyField(
        model_references.LESSON_DATA,
        verbose_name=model_verbose_functions.lesson_data_single,
    )
    
    designation = models.CharField(
        max_length=maxlength.TIMETABLE_DESIGNATION,
        verbose_name=_("Bezeichnung"),
        help_text=_("Die Bezeichnung für den Stundenplan"),
        blank=True
    )  # type: str
    
    school_year = models.PositiveSmallIntegerField(
        verbose_name=_("Schuljahr"),
        help_text=_("Das Jahr, indem das Schuljahr startet.")
    )
    
    def __str__(self):
        return self.designation
    
    @hook(BEFORE_CREATE)
    @hook(BEFORE_UPDATE, when="designation")
    def _hook_constrain_designation(self):
        self.designation = self.designation or create_designation_from_date()
    
    @hook(BEFORE_CREATE)
    @hook(BEFORE_UPDATE, when="lessons")
    def _hook_validate_lessons_dont_overlap(self):
        validate_lessons_dont_overlap(self.lessons_data.all())
