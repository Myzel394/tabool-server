from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import RandomIDMixin

from apps.django.utils.models import UserModelRelationMixin
from ...public import model_references, model_verbose_functions

if TYPE_CHECKING:
    from ...models import Homework

__all__ = [
    "UserHomeworkRelation"
]


class UserHomeworkRelation(RandomIDMixin, UserModelRelationMixin):
    class Meta:
        verbose_name = _("Benutzer-Hausaufgabe-Beziehung")
        verbose_name_plural = _("Benutzer-Hausaufgaben-Beziehungen")
        unique_together = (
            ("homework", "user")
        )
        ordering = ("homework", "user")
    
    homework = models.ForeignKey(
        model_references.HOMEWORK,
        verbose_name=model_verbose_functions.homework_single,
        on_delete=models.CASCADE,
    )  # type: Homework
    
    completed = models.BooleanField(
        default=False,
        verbose_name=_("Erledigt")
    )  # type: bool
    
    ignore = models.BooleanField(
        default=False,
        verbose_name=_("Ignorieren")
    )
    
    def __str__(self):
        return str(self.homework)
