from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.handlers.mixins import WhiteSpaceStripHandler
from django_common_utils.libraries.handlers.models import HandlerMixin
from django_common_utils.libraries.models.mixins import RandomIDMixin
from django_hint import QueryType

from constants import maxlength
from ..options import GenderChoices
from ..public import model_names

if TYPE_CHECKING:
    from apps.django.main.lesson.models import LessonData

__all__ = [
    "Teacher"
]


class Teacher(RandomIDMixin, HandlerMixin):
    class Meta:
        verbose_name = model_names.TEACHER
        verbose_name_plural = model_names.TEACHER_PLURAL
        ordering = ("last_name", "first_name", "short_name", "email")
    
    first_name = models.CharField(
        verbose_name=_("Vorname"),
        blank=True,
        null=True,
        max_length=maxlength.FIRST_NAME,
    )  # type: str
    
    last_name = models.CharField(
        verbose_name=_("Letzter Name"),
        max_length=maxlength.SECOND_NAME
    )  # type: str
    
    short_name = models.CharField(
        verbose_name=_("Kürzel"),
        max_length=3,
        blank=True,
        null=True
    )  # type: str
    
    email = models.EmailField(
        verbose_name=_("E-Mail"),
        blank=True,
        null=True
    )  # type: str
    
    gender = models.PositiveSmallIntegerField(
        choices=GenderChoices.choices,
        verbose_name=_("Geschlecht"),
        default=GenderChoices.UNKNOWN
    )  # type: int
    
    def __str__(self):
        return _("{first_name} {last_name}, {short_name}").format(
            first_name=self.first_name,
            last_name=self.last_name,
            short_name=self.short_name
        )
    
    @property
    def lessons_data(self) -> QueryType["LessonData"]:
        return self.lessons_data.all()
    
    @staticmethod
    def handlers():
        return {
            ("first_name", "last_name"): WhiteSpaceStripHandler()
        }
