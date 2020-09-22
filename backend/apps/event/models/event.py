from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.handlers import HandlerMixin, WhiteSpaceStripHandler
from django_common_utils.libraries.models import RandomIDMixin

from apps.subject import model_references, model_verbose_functions
from constants import maxlength

__all__ = [
    "Event"
]


class Event(RandomIDMixin, HandlerMixin):
    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
    
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
