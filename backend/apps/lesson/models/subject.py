from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.handlers.mixins import WhiteSpaceStripHandler
from django_common_utils.libraries.handlers.models import HandlerMixin
from django_common_utils.libraries.models.mixins import RandomIDMixin
from django_hint import QueryType

from apps.utils.models import ColorMixin
from constants import maxlength
from ..querysets import SubjectQuerySet

if TYPE_CHECKING:
    from ..models import Lesson

__all__ = [
    "Subject"
]


class Subject(RandomIDMixin, ColorMixin, HandlerMixin):
    class Meta:
        verbose_name = _("Fach")
        verbose_name_plural = _("Fächer")
        ordering = ("name",)
    
    objects = SubjectQuerySet.as_manager()
    
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=maxlength.SUBJECT
    )  # type: str
    
    short_name = models.CharField(
        verbose_name=_("Kurzer Name"),
        max_length=15,
    )  # type: str
    
    def __str__(self):
        return self.name
    
    @property
    def lessons_data(self) -> QueryType["Lesson"]:
        return self.lessondata_set.all()
    
    @staticmethod
    def handlers():
        return {
            "name": WhiteSpaceStripHandler()
        }
