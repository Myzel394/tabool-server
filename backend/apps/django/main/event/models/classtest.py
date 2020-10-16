from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.handlers.mixins import TextOptimizerHandler
from django_common_utils.libraries.handlers.models import HandlerMixin
from django_common_utils.libraries.models.mixins import CreationDateMixin, RandomIDMixin
from django_lifecycle import BEFORE_CREATE, BEFORE_UPDATE, hook, LifecycleModel
from simple_history.models import HistoricalRecords

from apps.django.utils.history_extras.extras import UserInformationHistoricalModel
from apps.django.utils.validators import validate_weekday_in_lesson_data_available
from apps.utils import format_datetime
from ..querysets import ClasstestQuerySet
from ...lesson.public import *
from ...school_data.public.model_references import ROOM
from ...school_data.public.model_verbose_functions import room_single

if TYPE_CHECKING:
    from datetime import date, datetime
    from apps.django.main.school_data.models import Room
    from apps.django.main.lesson import Course

__all__ = [
    "Classtest"
]


class Classtest(RandomIDMixin, CreationDateMixin, LifecycleModel, HandlerMixin):
    class Meta:
        verbose_name = _("Klassenarbeit")
        verbose_name_plural = _("Klassenarbeiten")
        ordering = ("targeted_date", "course", "room")
    
    objects = ClasstestQuerySet.as_manager()
    
    course = models.ForeignKey(
        COURSE,
        on_delete=models.CASCADE,
        verbose_name=course_single,
    )  # type: Course
    
    room = models.ForeignKey(
        ROOM,
        on_delete=models.CASCADE,
        verbose_name=room_single,
        blank=True,
        null=True
    )  # type: Room
    
    targeted_date = models.DateField(
        verbose_name=_("Datum"),
        help_text=_("Datum, wann die Klassenarbeit geschrieben wird.")
    )  # type: date
    
    information = models.TextField(
        verbose_name=_("Informationen"),
        blank=True,
        null=True
    )  # type: str
    
    history = HistoricalRecords(
        cascade_delete_history=True,
        bases=[UserInformationHistoricalModel]
    )
    
    def __str__(self):
        return _("{course} am {targeted_date}").format(
            course_str=self.course,
            targeted_date=format_datetime(self.targeted_date)
        )
    
    @staticmethod
    def handlers():
        return {
            "information": TextOptimizerHandler()
        }
    
    @hook(BEFORE_CREATE)
    @hook(BEFORE_UPDATE, when="targeted_date")
    def _hook_validate_targeted_dae(self):
        validate_weekday_in_lesson_data_available(self.targeted_date)
    
    @property
    def edited_at(self) -> "datetime":
        return self.history.latest().history_date
