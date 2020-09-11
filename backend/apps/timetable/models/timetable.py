from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models import RandomIDMixin
from django_common_utils.libraries.utils import model_verbose
from django_lifecycle import BEFORE_CREATE, BEFORE_UPDATE, hook, LifecycleModel

from apps.utils.models import AssociatedUserMixin
from constants import maxlength
from .. import constants
from ..utils import create_designation_from_date

__all__ = [
    "TimeTable"
]


class TimeTable(RandomIDMixin, AssociatedUserMixin, LifecycleModel):
    class Meta:
        verbose_name = _("Stundenplan")
        verbose_name_plural = _("Stundenpläne")
        ordering = ("designation",)
        unique_together = (
            ("associated_user", "designation")
        )
        app_label = constants.APP_LABEL
    
    lessons = models.ManyToManyField(
        "Lesson",
        verbose_name=model_verbose(f"{constants.APP_LABEL}.Lesson")
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
    
    @staticmethod
    def Easy_create(**kwargs) -> "TimeTable":
        lessons = kwargs.pop("lessons")
        
        timetable = TimeTable.objects.create(
            **kwargs
        )
        timetable.lessons.add(lessons)
        
        return timetable
