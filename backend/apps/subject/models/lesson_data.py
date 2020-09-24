from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models import RandomIDMixin
from django_hint import QueryType

from apps.utils.fields.weekday import WeekdayField
from apps.utils.time import dummy_datetime_from_time, format_datetime
from .. import constants
from ..public import model_references, model_verbose_functions
from ..sub.subquerysets import LessonQuerySet
from ..sub.subquerysets.lesson_data import LessonDataQuerySet

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
        ordering = ("subject", "start_time")
    
    objects = LessonDataQuerySet.as_manager()
    
    teacher = models.ForeignKey(
        model_references.TEACHER,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=model_verbose_functions.teacher_single,
    )
    
    room = models.ForeignKey(
        model_references.ROOM,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=model_verbose_functions.room_single,
    )
    
    subject = models.ForeignKey(
        model_references.SUBJECT,
        on_delete=models.CASCADE,
        verbose_name=model_verbose_functions.subject_single,
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
    
    def __str__(self):
        return f"{self.subject}: {format_datetime(self.start_time)} - {format_datetime(self.end_time)}"
    
    @property
    def duration(self) -> int:
        """Returns the duration of the lesson in minutes"""
        difference = dummy_datetime_from_time(self.end_time) - dummy_datetime_from_time(self.start_time)
        
        return int(difference.seconds / 60)
    
    @property
    def teacher_homeworks(self) -> QueryType["TeacherHomework"]:
        return self.teacherhomework_set.all()
    
    @property
    def user_homeworks(self) -> QueryType["Homework"]:
        return self.userhomework_set.all()
    
    @property
    def homeworks(self) -> QueryType[Union["TeacherHomework", "Homework"]]:
        return self.teacher_homeworks | self.associated_user_id
    
    def get_lesson(self, **kwargs) -> "Lesson":
        return LessonQuerySet.create_automatically(
            lesson_data=self,
            **kwargs
        )
