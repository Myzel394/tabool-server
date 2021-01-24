from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.handlers.mixins import TextOptimizerHandler
from django_common_utils.libraries.handlers.models import HandlerMixin
from django_common_utils.libraries.models.mixins import RandomIDMixin

from ..public import *
from ..public import model_names

__all__ = [
    "Classbook"
]


class Classbook(RandomIDMixin, HandlerMixin):
    class Meta:
        verbose_name = model_names.CLASSBOOK
        verbose_name_plural = model_names.CLASSBOOK_PLURAL
        ordering = ("lesson",)
    
    lesson = models.OneToOneField(
        LESSON,
        verbose_name=model_names.LESSON,
        on_delete=models.CASCADE,
    )
    
    presence_content = models.TextField(
        verbose_name=_("Inhalt Präsenzunterricht"),
        null=True,
    )
    distance_content = models.TextField(
        verbose_name=_("Inhalt Fernunterricht"),
        null=True,
    )
    
    @staticmethod
    def handlers():
        return {
            "presence_content": TextOptimizerHandler(),
            "distance_content": TextOptimizerHandler()
        }
