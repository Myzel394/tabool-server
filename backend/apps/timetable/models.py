from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.handlers.mixins import WhiteSpaceStripHandler
from django_common_utils.libraries.models import HandlerMixin, RandomIDMixin
from django_common_utils.libraries.utils import model_verbose, model_verbose_plural
from django_hint import QueryType
from django_lifecycle import BEFORE_CREATE, BEFORE_UPDATE, hook, LifecycleModel

from apps.utils.fields.weekday import WeekdayField
from apps.utils.time import dummy_datetime_from_time, format_datetime
from apps.utils.validators import validate_place
from constants import maxlength
from .constants import LESSON_ALLOWED_DAYS
from .utils import create_designation_from_date
from ..utils.models import AssociatedUserMixin, ColorMixin

__all__ = [
    "Teacher", "Subject", "Room", "Lesson", "TimeTable"
]


class Teacher(RandomIDMixin, HandlerMixin):
    class Meta:
        verbose_name = _("Lehrer")
        verbose_name_plural = _("Lehrer")
        ordering = ("last_name", "first_name", "email")
    
    first_name = models.CharField(
        verbose_name=_("Vorname"),
        blank=True,
        null=True,
        max_length=maxlength.FIRST_NAME,
    )
    
    last_name = models.CharField(
        verbose_name=_("Letzter Name"),
        max_length=maxlength.SECOND_NAME
    )
    
    email = models.EmailField(
        verbose_name=_("E-Mail"),
        blank=True,
        null=True
    )
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def lessons(self) -> QueryType["Lesson"]:
        return self.lesson_set.all()
    
    @staticmethod
    def handlers():
        return {
            ("first_name", "last_name"): WhiteSpaceStripHandler()
        }


class Subject(RandomIDMixin, HandlerMixin, ColorMixin):
    class Meta:
        verbose_name = _("Fach")
        verbose_name_plural = _("Fächer")
        ordering = ("name",)
    
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=maxlength.SUBJECT
    )
    
    def __str__(self):
        return self.name
    
    @property
    def lessons(self) -> QueryType["Lesson"]:
        return self.lesson_set.all()
    
    @staticmethod
    def handlers():
        return {
            "name": WhiteSpaceStripHandler()
        }


class Room(RandomIDMixin, LifecycleModel):
    class Meta:
        verbose_name = _("Raum")
        verbose_name_plural = _("Räume")
        ordering = ("place",)
    
    place = models.CharField(
        verbose_name=_("Ort"),
        max_length=maxlength.ROOM
    )  # type: str
    
    def __str__(self):
        return f"{model_verbose(self.__class__)}: {self.place}"
    
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
    
    @hook(BEFORE_CREATE)
    @hook(BEFORE_UPDATE, when="place")
    def _hook_place_validation_and_constraining(self):
        self.place = self.place.capitalize()
        validate_place(self.place)
    
    @property
    def lessons(self) -> QueryType["Lesson"]:
        return self.lesson_set.all()


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


class TimeTable(RandomIDMixin, AssociatedUserMixin, LifecycleModel):
    class Meta:
        verbose_name = _("Stundenplan")
        verbose_name_plural = _("Stundenpläne")
        unique_together = (
            ("associated_user", "designation")
        )
    
    lessons = models.ManyToManyField(
        Lesson,
        verbose_name=model_verbose_plural(Lesson)
    )
    
    designation = models.CharField(
        max_length=maxlength.TIMETABLE_DESIGNATION,
        verbose_name=_("Bezeichnung"),
        help_text=_("Die Bezeichnung für den Stundenplan"),
        blank=True
    )
    
    @hook(BEFORE_CREATE)
    @hook(BEFORE_UPDATE, when="designation")
    def _hook_constrain_designation(self):
        self.designation = self.designation or create_designation_from_date()
    
    @staticmethod
    def Easy_create(**kwargs) -> "TimeTable":
        lessons = kwargs.pop("lessons")
        
        timetable = TimeTable.objects.create(
            **kwargs
        )
        timetable.lessons.add(lessons)
        
        return timetable
