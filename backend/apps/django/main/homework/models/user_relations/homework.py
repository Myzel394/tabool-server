from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import RandomIDMixin

from apps.django.utils.models import UserModelRelationMixin
from ...public import *
from ...public import model_names

if TYPE_CHECKING:
    from ...models import Homework

__all__ = [
    "UserHomeworkRelation"
]


class UserHomeworkRelation(RandomIDMixin, UserModelRelationMixin):
    class Meta:
        verbose_name = model_names.HOMEWORK_RELATION
        verbose_name_plural = model_names.HOMEWORK_RELATION_PLURAL
        unique_together = (
            ("homework", "user")
        )
        ordering = ("homework", "user")
    
    homework = models.ForeignKey(
        HOMEWORK,
        on_delete=models.CASCADE,
        verbose_name=model_names.HOMEWORK
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
