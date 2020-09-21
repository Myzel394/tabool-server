from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.handlers import HandlerMixin, WhiteSpaceStripHandler
from django_common_utils.libraries.models import RandomIDMixin
from django_hint import QueryType

from apps.utils.models import ColorMixin
from constants import maxlength

if TYPE_CHECKING:
    from apps.timetable.models import Lesson

__all__ = [
    "Subject"
]

# TODO: Subject zu eigener App machen mit Homework, Vertretungen (Substitute) etc..


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
