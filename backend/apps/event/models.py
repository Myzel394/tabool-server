from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.handlers import HandlerMixin
from django_common_utils.libraries.handlers.mixins import TextOptimizerHandler, WhiteSpaceStripHandler
from django_common_utils.libraries.models import RandomIDMixin
from django_common_utils.libraries.utils import model_verbose

from apps.lesson import constants as subject_constants
from apps.lesson.models import Room
from apps.utils.time import format_datetime
from .choices import *


class Event(RandomIDMixin, HandlerMixin):
    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
        ordering = ("start_datetime",)
    
    room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    
    event_type = models.PositiveSmallIntegerField(
        choices=EventTypeChoices.choices,
        default=EventTypeChoices.EVENT,
        verbose_name=_("Eventtyp")
    )
    
    start_datetime = models.DateTimeField(
        verbose_name=_("Startzeit"),
    )
    
    end_datetime = models.DateTimeField(
        verbose_name=_("Endzeit")
    )
    
    information = models.TextField(
        verbose_name=_("Information"),
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


def _classtest_lesson_model_verbose():
    return model_verbose(f"{subject_constants.APP_LABEL}.Lesson")


class ClassTest(RandomIDMixin):
    class Meta:
        verbose_name = _("Klassenarbeit")
        verbose_name_plural = _("Klassenarbeiten")
    
    lesson = models.ForeignKey(
        f"{subject_constants.APP_LABEL}.Lesson",
        on_delete=models.CASCADE,
        verbose_name=_classtest_lesson_model_verbose
    )
