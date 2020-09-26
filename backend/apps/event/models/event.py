from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.handlers import HandlerMixin, WhiteSpaceStripHandler
from django_common_utils.libraries.models import RandomIDMixin
from django_lifecycle import BEFORE_CREATE, BEFORE_UPDATE, hook

from apps.lesson.public import model_references, model_verbose_functions  # TODO: Import these as *
from apps.utils.validators import validate_weekday_in_lesson_data_available
from constants import maxlength
from .user_relations.event import UserEventRelation
from ...utils import RelationMixin

__all__ = [
    "Event"
]


class Event(RandomIDMixin, HandlerMixin, RelationMixin):
    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
        ordering = ("title", "start_datetime", "end_datetime", "room")
    
    get_relation: UserEventRelation
    RELATED_MODEL = UserEventRelation
    
    room = models.ForeignKey(
        model_references.ROOM,
        verbose_name=model_verbose_functions.room_single,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    
    title = models.CharField(
        verbose_name=_("Titel"),
        max_length=maxlength.TITLE
    )
    
    start_datetime = models.DateTimeField(
        verbose_name=_("Start")
    )
    
    end_datetime = models.DateTimeField(
        verbose_name=_("Ende")
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
