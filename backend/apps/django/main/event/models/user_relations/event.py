from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import RandomIDMixin

from apps.django.utils.models import UserModelRelationMixin
from ...public import *
from ...public import model_names

if TYPE_CHECKING:
    from .. import Event

__all__ = [
    "UserEventRelation"
]


class UserEventRelation(RandomIDMixin, UserModelRelationMixin):
    class Meta:
        verbose_name = model_names.EVENT_RELATION
        verbose_name_plural = model_names.EVENT_RELATION_PLURAL
        unique_together = (
            ("event", "user")
        )
        ordering = ("event", "user")
    
    event = models.ForeignKey(
        EVENT,
        on_delete=models.CASCADE,
        verbose_name=model_names.EVENT
    )  # type: Event
    
    ignore = models.BooleanField(
        default=False,
        verbose_name=_("Ignorieren"),
    )  # type: bool
    
    def __str__(self):
        return str(self.event)
