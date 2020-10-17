from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.handlers.mixins import WhiteSpaceStripHandler
from django_common_utils.libraries.handlers.models import HandlerMixin
from django_common_utils.libraries.models.mixins import RandomIDMixin
from django_hint import QueryType

from apps.django.utils.models import ColorMixin
from constants import maxlength
from ..public import model_verboses
from ..querysets import SubjectQuerySet

if TYPE_CHECKING:
    from apps.django.main.lesson.models import Lesson

__all__ = [
    "Subject"
]


class Subject(RandomIDMixin, ColorMixin, HandlerMixin):
    class Meta:
        verbose_name = model_verboses.SUBJECT
        verbose_name_plural = model_verboses.SUBJECT_PLURAL
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
        # noinspection PyUnresolvedReferences
        return self.lessondata_set.all()
    
    @staticmethod
    def handlers():
        return {
            "name": WhiteSpaceStripHandler()
        }
