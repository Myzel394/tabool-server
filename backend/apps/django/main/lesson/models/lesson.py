from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import RandomIDMixin
from django_lifecycle import LifecycleModel

from apps.django.main.school_data.public import model_names as school_names, model_references as school_references
from apps.utils import format_datetime
from ..public import *
from ..public import model_names
from ..querysets import LessonQuerySet

if TYPE_CHECKING:
    from datetime import date as typing_date, time
    from . import Course
    from apps.django.main.school_data.models import Room

__all__ = [
    "Lesson"
]


class Lesson(RandomIDMixin, LifecycleModel):
    class Meta:
        verbose_name = model_names.LESSON
        verbose_name_plural = model_names.LESSON_PLURAL
        ordering = ("date", "start_time", "end_time")
    
    objects = LessonQuerySet.as_manager()
    
    date = models.DateField(
        verbose_name=_("Datum")
    )  # type: typing_date
    
    video_conference_link = models.URLField(
        max_length=1023,
        verbose_name=_("Videokonferenz-Link"),
        blank=True,
        null=True
    )
    
    course = models.ForeignKey(
        COURSE,
        on_delete=models.CASCADE,
        verbose_name=model_names.COURSE,
    )  # type: Course
    
    room = models.ForeignKey(
        school_references.ROOM,
        on_delete=models.SET_NULL,
        verbose_name=school_names.ROOM,
        blank=True,
        null=True,
    )  # type: Room
    
    start_time = models.TimeField(
        verbose_name=_("Startzeit"),
    )  # type: time
    
    end_time = models.TimeField(
        verbose_name=_("Endzeit"),
    )  # type: time
    
    def __str__(self):
        return _("{date}, {course}").format(
            date=format_datetime(self.date),
            course=self.course
        )
    
    @property
    def weekday(self) -> int:
        return self.date.weekday()
