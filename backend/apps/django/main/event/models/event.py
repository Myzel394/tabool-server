from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.handlers.mixins import WhiteSpaceStripHandler
from django_common_utils.libraries.handlers.models import HandlerMixin
from django_common_utils.libraries.models.mixins import CreationDateMixin, RandomIDMixin
from django_hint import QueryType
from django_lifecycle import BEFORE_CREATE, BEFORE_UPDATE, hook

from apps.django.utils.validators import validate_weekday_in_lesson_data_available
from apps.utils import format_datetime
from constants import maxlength
from ..sub.subquerysets import EventQuerySet
from ...school_data.public.model_references import ROOM
from ...school_data.public.model_verbose_functions import room_single

if TYPE_CHECKING:
    from datetime import datetime, time, timedelta
    from apps.django.main.school_data.models import Room
    from . import UserEventRelation

__all__ = [
    "Event"
]


class Event(RandomIDMixin, CreationDateMixin, HandlerMixin):
    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
        ordering = ("title", "start_datetime", "end_datetime", "room")
    
    objects = EventQuerySet.as_manager()
    
    room = models.ForeignKey(
        ROOM,
        verbose_name=room_single,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )  # type: Room
    
    title = models.CharField(
        verbose_name=_("Titel"),
        max_length=maxlength.TITLE
    )  # type: str
    
    start_datetime = models.DateTimeField(
        verbose_name=_("Start")
    )  # type: datetime
    
    end_datetime = models.DateTimeField(
        verbose_name=_("Ende")
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
    @hook(BEFORE_UPDATE, when_any=["start_datetime", "end_datetime"])
    def _hook_validate_dates(self):
        validate_weekday_in_lesson_data_available(self.start_datetime)
        validate_weekday_in_lesson_data_available(self.end_datetime)
    
    @property
    def user_relations(self) -> QueryType["UserEventRelation"]:
        return self.usereventrelation_set.all()
    
    @property
    def is_all_day(self) -> bool:
        start_datetime_begin = datetime.combine(
            self.start_datetime.date(),
            time.min
        )
        
        return start_datetime_begin + timedelta(days=1) == self.end_datetime
