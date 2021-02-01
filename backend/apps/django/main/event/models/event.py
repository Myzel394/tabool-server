from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.handlers.mixins import WhiteSpaceStripHandler
from django_common_utils.libraries.handlers.models import HandlerMixin
from django_common_utils.libraries.models.mixins import RandomIDMixin
from django_lifecycle import BEFORE_CREATE, BEFORE_UPDATE, hook, LifecycleModel

from apps.django.main.school_data.public import model_names as school_names
from apps.django.utils.validators import validate_weekday_in_lesson_data_available
from apps.utils import format_datetime, is_all_day
from constants import maxlength
from ..public import model_names
from ..sub.subquerysets import EventQuerySet
from ...school_data.public.model_references import *

if TYPE_CHECKING:
    from datetime import datetime
    from apps.django.main.school_data.models import Room

__all__ = [
    "Event"
]


class Event(RandomIDMixin, HandlerMixin, LifecycleModel):
    class Meta:
        verbose_name = model_names.EVENT
        verbose_name_plural = model_names.EVENT_PLURAL
        ordering = ("title", "start_datetime", "end_datetime", "room")
    
    objects = EventQuerySet.as_manager()
    
    room = models.ForeignKey(
        ROOM,
        on_delete=models.SET_NULL,
        verbose_name=school_names.ROOM,
        blank=True,
        null=True,
    )  # type: Room
    
    title = models.CharField(
        verbose_name=_("Titel"),
        max_length=maxlength.TITLE
    )  # type: str
    
    start_datetime = models.DateTimeField(
        verbose_name=_("Start"),
        validators=[validate_weekday_in_lesson_data_available]
    )  # type: datetime
    
    end_datetime = models.DateTimeField(
        verbose_name=_("Ende"),
        validators=[validate_weekday_in_lesson_data_available]
    )  # type: datetime
    
    def __str__(self):
        return _("{title} vom {start_datetime} bis {end_datetime}").format(
            title=self.title,
            start_datetime=format_datetime(self.start_datetime),
            end_datetime=format_datetime(self.end_datetime)
        )
    
    @staticmethod
    def handlers():
        return {
            "title": WhiteSpaceStripHandler()
        }
    
    @hook(BEFORE_CREATE)
    @hook(BEFORE_UPDATE, when_any=["start_datetime", "end_datetime"], has_changed=True)
    def _hook_full_clean(self):
        self.full_clean()
    
    @property
    def is_all_day(self) -> bool:
        return is_all_day(self.start_datetime, self.end_datetime)
