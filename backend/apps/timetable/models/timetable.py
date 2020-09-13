from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models import CustomQuerySetMixin, RandomIDMixin
from django_common_utils.libraries.utils import model_verbose
from django_lifecycle import BEFORE_CREATE, BEFORE_UPDATE, hook, LifecycleModel

from apps.timetable import constants
from apps.timetable.querysets import TimeTableQuerySet
from apps.timetable.utils import create_designation_from_date
from apps.utils.models import AssociatedUserMixin
from constants import maxlength

__all__ = [
    "TimeTable"
]


def _timetable_lessons_model_verbose():
    return model_verbose(f"{constants.APP_LABEL}.Lesson")


class TimeTable(RandomIDMixin, AssociatedUserMixin, LifecycleModel, CustomQuerySetMixin):
    class Meta:
        verbose_name = _("Stundenplan")
        verbose_name_plural = _("Stundenpläne")
        ordering = ("designation",)
        unique_together = (
            ("associated_user", "designation")
        )
    
    objects = TimeTableQuerySet.as_manager()
    
    lessons = models.ManyToManyField(
        "Lesson",
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
