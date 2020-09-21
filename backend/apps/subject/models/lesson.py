from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models import RandomIDMixin
from django_common_utils.libraries.utils import model_verbose
from django_hint import QueryType

from apps.timetable import constants
from apps.utils.fields.weekday import WeekdayField
from apps.utils.time import dummy_datetime_from_time, format_datetime

if TYPE_CHECKING:
    from apps.homework.models import Homework, UserHomework

__all__ = [
    "Lesson",
]


def _lesson_teacher_model_verbose():
    return model_verbose(f"{constants.APP_LABEL}.Teacher")


def _lesson_room_model_verbose():
    return model_verbose(f"{constants.APP_LABEL}.Room")


def _lesson_subject_model_verbose():
    return model_verbose(f"{constants.APP_LABEL}.Subject")


class Lesson(RandomIDMixin):
    class Meta:
        verbose_name = _("Stunde")
        verbose_name_plural = _("Stunden")
        ordering = ("subject", "start_time")
    
    teacher = models.ForeignKey(
        "Teacher",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_lesson_teacher_model_verbose
    )
    
    room = models.ForeignKey(
        "Room",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_lesson_room_model_verbose
    )
    
    subject = models.ForeignKey(
        "Subject",
        on_delete=models.CASCADE,
        verbose_name=_lesson_subject_model_verbose
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
    def homeworks(self) -> QueryType[Union["Homework", "UserHomework"]]:
        return self.homework_set.all() | self.userhomework_set.all()
