from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models import CustomQuerySetMixin, RandomIDMixin
from django_common_utils.libraries.utils import model_verbose
from django_lifecycle import BEFORE_CREATE, BEFORE_UPDATE, hook, LifecycleModel

from apps.subject import constants as subject_constants
from apps.timetable.utils import create_designation_from_date
from constants import maxlength
from ..sub.subquerysets import TimeTableQuerySet
from ..validators import validate_lessons_dont_overlap
from apps.subject import model_references, model_verbose_functions

if TYPE_CHECKING:
    from apps.subject.querysets import LessonQuerySet
    from apps.subject.models import Lesson

__all__ = [
    "TimeTable"
]


class TimeTable(
    RandomIDMixin,
    LifecycleModel,
    CustomQuerySetMixin
):
    class Meta:
        verbose_name = _("Stundenplan")
        verbose_name_plural = _("Stundenpläne")
        ordering = ("designation",)
    
    objects = TimeTableQuerySet.as_manager()
    
    lessons_data = models.ManyToManyField(
        model_references.LESSON_DATA,
        verbose_name=model_verbose_functions.lesson_data_single,
    )
    
    designation = models.CharField(
        max_length=maxlength.TIMETABLE_DESIGNATION,
        verbose_name=_("Bezeichnung"),
        help_text=_("Die Bezeichnung für den Stundenplan"),
        blank=True
    )
    
    @hook(BEFORE_CREATE)
    @hook(BEFORE_UPDATE, when="designation")
    def _hook_constrain_designation(self):
        self.designation = self.designation or create_designation_from_date()
    
    @hook(BEFORE_CREATE)
    @hook(BEFORE_UPDATE, when="lessons")
    def _hook_validate_lessons_dont_overlap(self):
        validate_lessons_dont_overlap(self.lessons.all())
