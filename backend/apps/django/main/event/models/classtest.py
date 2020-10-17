from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.handlers.mixins import TextOptimizerHandler
from django_common_utils.libraries.handlers.models import HandlerMixin
from django_common_utils.libraries.models.mixins import CreationDateMixin, RandomIDMixin
from django_lifecycle import BEFORE_CREATE, BEFORE_UPDATE, hook, LifecycleModel
from simple_history.models import HistoricalRecords

from apps.django.main.lesson.public import model_verboses as lesson_verbose
from apps.django.main.school_data.public import model_verboses as school_verbose
from apps.django.utils.history_extras.extras import UserInformationHistoricalModel
from apps.django.utils.validators import validate_weekday_in_lesson_data_available
from apps.utils import format_datetime
from ..public import model_verboses
from ..querysets import ClasstestQuerySet
from ...lesson.public.model_references import *
from ...school_data.public.model_references import *

if TYPE_CHECKING:
    from datetime import date, datetime
    from apps.django.main.school_data.models import Room
    from apps.django.main.lesson.models import Course

__all__ = [
    "Classtest"
]


class Classtest(RandomIDMixin, CreationDateMixin, LifecycleModel, HandlerMixin):
    class Meta:
        verbose_name = model_verboses.CLASSTEST
        verbose_name_plural = model_verboses.CLASSTEST_PLURAL
        ordering = ("targeted_date", "course", "room")
    
    objects = ClasstestQuerySet.as_manager()
    
    course = models.ForeignKey(
        COURSE,
        on_delete=models.CASCADE,
        verbose_name=lesson_verbose.COURSE
    )  # type: Course
    
    room = models.ForeignKey(
        ROOM,
        on_delete=models.CASCADE,
        verbose_name=school_verbose.ROOM,
        blank=True,
        null=True
    )  # type: Room
    
    targeted_date = models.DateField(
        verbose_name=_("Datum"),
        help_text=_("Datum, wann die Klassenarbeit geschrieben wird."),
        validators=[validate_weekday_in_lesson_data_available]
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
            course=self.course,
            targeted_date=format_datetime(self.targeted_date)
        )
    
    @staticmethod
    def handlers():
        return {
            "information": TextOptimizerHandler()
        }
    
    @hook(BEFORE_CREATE)
    @hook(BEFORE_UPDATE, when="targeted_date", has_changed=True)
    def _hook_full_clean(self):
        self.full_clean()
    
    @property
    def edited_at(self) -> "datetime":
        return self.history.latest().history_date
