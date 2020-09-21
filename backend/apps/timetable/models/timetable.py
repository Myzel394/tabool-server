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

__all__ = [
    "TimeTable"
]


def _timetable_lessons_model_verbose():
    return model_verbose(f"{subject_constants.APP_LABEL}.Lesson")


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
    
    lessons = models.ManyToManyField(
        f"{subject_constants.APP_LABEL}.Lesson",
        verbose_name=_timetable_lessons_model_verbose
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
