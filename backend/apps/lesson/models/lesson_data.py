from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import RandomIDMixin

import apps.school_data.public.model_references
import apps.school_data.public.model_verbose_functions
from apps.utils.fields.weekday import WeekdayField
from apps.utils.time import dummy_datetime_from_target
from constants import weekdays
from .lesson import Lesson
from ..public import model_references, model_verbose_functions
from ..sub.subquerysets import LessonDataQuerySet

if TYPE_CHECKING:
    from datetime import time
    from . import Room, Course

__all__ = [
    "LessonData",
]


class LessonData(RandomIDMixin):
    class Meta:
        verbose_name = _("Stunde")
        verbose_name_plural = _("Stunden")
        ordering = ("course", "start_time")
    
    objects = LessonDataQuerySet.as_manager()
    
    room = models.ForeignKey(
        apps.school_data.public.model_references.ROOM,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=apps.school_data.public.model_verbose_functions.room_single,
    )  # type: Room
    
    course = models.ForeignKey(
        model_references.COURSE,
        on_delete=models.CASCADE,
        verbose_name=model_verbose_functions.course_single,
    )  # type: Course
    
    start_time = models.TimeField(
        verbose_name=_("Startzeit"),
    )  # type: time
    
    end_time = models.TimeField(
        verbose_name=_("Endzeit"),
    )  # type: time
    
    weekday = WeekdayField(
        verbose_name=_("Wochentag"),
        choices=weekdays.ALLOWED_WEEKDAYS
    )  # type: int
    
    @property
    def duration(self) -> int:
        """Returns the duration of the lesson in minutes"""
        difference = dummy_datetime_from_target(self.end_time) - dummy_datetime_from_target(self.start_time)
        
        return int(difference.seconds / 60)
    
    def create_lesson(self, **kwargs) -> Lesson:
        return Lesson.objects.create_automatically(
            lesson_data=self,
            **kwargs
        )
