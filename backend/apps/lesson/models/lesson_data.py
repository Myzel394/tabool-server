from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models import RandomIDMixin
from django_hint import QueryType

from apps.utils.fields.weekday import WeekdayField
from apps.utils.time import dummy_datetime_from_time, format_datetime
from .lesson import Lesson
from .. import constants
from ..public import model_references, model_verbose_functions
from ..sub.subquerysets import LessonDataQuerySet

if TYPE_CHECKING:
    from apps.homework.models import TeacherHomework, Homework
    from .lesson import Lesson

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
        model_references.ROOM,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=model_verbose_functions.room_single,
    )
    
    course = models.ForeignKey(
        model_references.COURSE,
        on_delete=models.CASCADE,
        verbose_name=model_verbose_functions.course_single,
    )
    
    start_time = models.TimeField(
        verbose_name=_("Startzeit"),
    )
    
    end_time = models.TimeField(
        verbose_name=_("Endzeit"),
    )
    
    weekday = WeekdayField(
        verbose_name=_("Wochentag"),
        choices=constants.LESSON_ALLOWED_DAYS
    )
    
    @property
    def duration(self) -> int:
        """Returns the duration of the lesson in minutes"""
        difference = dummy_datetime_from_time(self.end_time) - dummy_datetime_from_time(self.start_time)
        
        return int(difference.seconds / 60)
    
    @property
    def homeworks(self) -> QueryType[Union["TeacherHomework", "Homework"]]:
        return self.homework_set.all()
    
    def create_lesson(self, **kwargs) -> "Lesson":
        return Lesson.objects.create_automatically(
            lesson_data=self,
            **kwargs
        )
