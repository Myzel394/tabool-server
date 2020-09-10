from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models import HandlerMixin, RandomIDMixin, WhiteSpaceStripHandler
from django_hint import QueryType

from apps.utils.models import ColorMixin
from constants import maxlength
from .. import constants

__all__ = [
    "Subject"
]


class Subject(RandomIDMixin, HandlerMixin, ColorMixin):
    class Meta:
        verbose_name = _("Fach")
        verbose_name_plural = _("Fächer")
        ordering = ("name",)
        app_label = constants.APP_LABEL
    
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
