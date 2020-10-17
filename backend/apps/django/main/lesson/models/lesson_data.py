from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import RandomIDMixin

from apps.django.main.school_data.public import *
from apps.django.main.school_data.public import model_verboses as school_verbose
from apps.django.utils.fields import WeekdayField
from apps.utils.time import dummy_datetime_from_target
from constants import weekdays
from .lesson import Lesson
from ..public import *
from ..public import model_verboses
from ..querysets import LessonDataQuerySet

if TYPE_CHECKING:
    from datetime import time
    from . import Course
    from apps.django.main.school_data.models import Room

__all__ = [
    "LessonData",
]


class LessonData(RandomIDMixin):
    class Meta:
        verbose_name = model_verboses.LESSON_DATA
        verbose_name_plural = model_verboses.LESSON_DATA_PLURAL
        ordering = ("course", "start_time")
    
    objects = LessonDataQuerySet.as_manager()
    
    course = models.ForeignKey(
        COURSE,
        on_delete=models.CASCADE,
        verbose_name=model_verboses.COURSE,
    )  # type: Course
    
    room = models.ForeignKey(
        ROOM,
        on_delete=models.SET_NULL,
        verbose_name=school_verbose.ROOM,
        blank=True,
        null=True,
    )  # type: Room
    
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
    
    def __str__(self):
        return _("{course}: {weekday} {start_time} - {end_time}").format(
            start_time=self.start_time,
            end_time=self.end_time,
            weekday=self.get_weekday_display(),
            course=self.course
        )
    
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
