from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.handlers.mixins import WhiteSpaceStripHandler
from django_common_utils.libraries.handlers.models import HandlerMixin
from django_common_utils.libraries.models.mixins import CreationDateMixin, RandomIDMixin
from django_hint import QueryType
from django_lifecycle import BEFORE_CREATE, BEFORE_UPDATE, hook

from apps.lesson.public import *
from apps.utils.validators import validate_weekday_in_lesson_data_available
from constants import maxlength
from ..sub.subquerysets import EventQuerySet

if TYPE_CHECKING:
    from datetime import datetime
    from apps.lesson.models import Room
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
