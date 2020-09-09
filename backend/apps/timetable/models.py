from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.handlers.mixins import WhiteSpaceStripHandler
from django_common_utils.libraries.models import HandlerMixin, RandomIDMixin
from django_common_utils.libraries.utils import model_verbose
from django_hint import QueryType
from django_lifecycle import BEFORE_CREATE, BEFORE_UPDATE, hook, LifecycleModel

from apps.utils.validators import validate_place
from constants import maxlength
from .utils import create_designation_from_date
from ..utils.models import AssociatedUserMixin, ColorMixin

__all__ = [
    "Teacher", "Subject", "Room", "TimeTable"
]


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


class TimeTable(RandomIDMixin, AssociatedUserMixin, LifecycleModel):
    class Meta:
        verbose_name = _("Stundenplan")
        verbose_name_plural = _("Stundenpläne")
        unique_together = (
            ("associated_user", "designation")
        )
    
    lessons = models.ManyToManyField(
        "Lesson",
        verbose_name="gf"
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
