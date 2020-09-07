from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.handlers import HandlerMixin
from django_common_utils.libraries.handlers.mixins import TextOptimizerHandler, WhiteSpaceStripHandler
from django_common_utils.libraries.models import RandomIDMixin

from apps.utils.time import format_datetime
from constants import maxlength


class Event(RandomIDMixin, HandlerMixin):
    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
        ordering = ("start_datetime",)
    
    start_datetime = models.DateTimeField(
        verbose_name=_("Startzeit"),
    )
    
    end_datetime = models.DateTimeField(
        verbose_name=_("Endzeit")
    )
    
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=maxlength.TITLE,
    )
    
    description = models.CharField(
        verbose_name=_("Beschreibung"),
        max_length=maxlength.DESCRIPTION,
        blank=True,
        null=True,
    )
    
    @staticmethod
    def handlers():
        return {
            "title": WhiteSpaceStripHandler(),
            "description": TextOptimizerHandler()
        }
    
    def __str__(self):
        return f"{self.title} ({format_datetime(self.start_datetime)} - {format_datetime(self.end_datetime)})"
