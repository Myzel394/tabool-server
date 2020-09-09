from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models import RandomIDMixin
from django_common_utils.libraries.utils import model_verbose
from django_hint import QueryType

from apps.lesson.constants import LESSON_ALLOWED_DAYS
from apps.timetable.models import Room, Subject, Teacher
from apps.utils.fields.weekday import WeekdayField
from apps.utils.time import dummy_datetime_from_time, format_datetime

__all__ = [
    "Lesson",
]


class Lesson(RandomIDMixin):
    class Meta:
        verbose_name = _("Stunde")
        verbose_name_plural = _("Stunden")
        ordering = ("subject", "start_time")
    
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=model_verbose(Teacher)
    )
    
    room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=model_verbose(Room)
    )
    
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        verbose_name=model_verbose(Subject)
    )
    
    start_time = models.TimeField(
        verbose_name=_("Startzeit"),
    )
    
    end_time = models.TimeField(
        verbose_name=_("Endzeit"),
    )
    
    weekday = WeekdayField(
        verbose_name=_("Wochentag"),
        choices=LESSON_ALLOWED_DAYS
    )
    
    def __str__(self):
        return f"{self.subject}: {format_datetime(self.start_time)} - {format_datetime(self.end_time)}"
    
    @property
    def duration(self) -> int:
        """Returns the duration of the lesson in minutes"""
        difference = dummy_datetime_from_time(self.end_time) - dummy_datetime_from_time(self.start_time)
        
        return int(difference.seconds / 60)
    
    @property
    def homeworks(self) -> QueryType["Homework"]:
        return self.homework_set.all()
