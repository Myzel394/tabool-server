from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.handlers.mixins import WhiteSpaceStripHandler
from django_common_utils.libraries.handlers.models import HandlerMixin
from django_common_utils.libraries.models.mixins import RandomIDMixin
from django_lifecycle import LifecycleModel

from ..public import model_names
from ..querysets import SubjectQuerySet

__all__ = [
    "Subject"
]


class Subject(RandomIDMixin, LifecycleModel, HandlerMixin):
    class Meta:
        verbose_name = model_names.SUBJECT
        verbose_name_plural = model_names.SUBJECT_PLURAL
        ordering = ("name",)
    
    objects = SubjectQuerySet.as_manager()
    
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=31
    )  # type: str
    
    short_name = models.CharField(
        verbose_name=_("Kurzer Name"),
        max_length=7,
    )  # type: str
    
    def __str__(self):
        return self.name
    
    @staticmethod
    def handlers():
        return {
            "name": WhiteSpaceStripHandler()
        }
