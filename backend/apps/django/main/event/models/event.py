from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.handlers.mixins import WhiteSpaceStripHandler
from django_common_utils.libraries.handlers.models import HandlerMixin
from django_common_utils.libraries.models.mixins import RandomIDMixin
from django_hint import QueryType
from django_lifecycle import BEFORE_CREATE, BEFORE_UPDATE, hook

from apps.django.main.school_data.public import model_verboses as  school_verbose
from apps.django.utils.validators import validate_weekday_in_lesson_data_available
from apps.utils import format_datetime
from constants import maxlength
from ..public import model_verboses
from ..sub.subquerysets import EventQuerySet
from ...school_data.public.model_references import *

if TYPE_CHECKING:
    from datetime import datetime, time
    from apps.django.main.school_data.models import Room
    from . import UserEventRelation

__all__ = [
    "Event"
]


class Event(RandomIDMixin, HandlerMixin):
    class Meta:
        verbose_name = model_verboses.EVENT
        verbose_name_plural = model_verboses.EVENT_PLURAL
        ordering = ("title", "start_datetime", "end_datetime", "room")
    
    objects = EventQuerySet.as_manager()
    
    room = models.ForeignKey(
        ROOM,
        on_delete=models.SET_NULL,
        verbose_name=school_verbose.ROOM,
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
    def user_relations(self) -> QueryType["UserEventRelation"]:
        return self.usereventrelation_set.all()
    
    @property
    def is_all_day(self) -> bool:
        return self.start_datetime == datetime.combine(self.start_datetime.date(), time.min) \
               and self.end_datetime == datetime.combine(self.end_datetime.date(), time.max)
