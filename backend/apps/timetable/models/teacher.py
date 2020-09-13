from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.handlers import HandlerMixin, WhiteSpaceStripHandler
from django_common_utils.libraries.models import RandomIDMixin
from django_hint import QueryType

from constants import maxlength

if TYPE_CHECKING:
    from apps.timetable import Lesson

__all__ = [
    "Teacher"
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
