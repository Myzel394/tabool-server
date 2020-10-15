from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import RandomIDMixin

from apps.utils import UserModelRelationMixin
from ...public import *

if TYPE_CHECKING:
    from .. import Event

__all__ = [
    "UserEventRelation"
]


class UserEventRelation(RandomIDMixin, UserModelRelationMixin):
    class Meta:
        verbose_name = _("Benutzer-Event-Beziehung")
        verbose_name_plural = _("Benutzer-Event-Beziehungen")
        unique_together = (
            ("event", "user")
        )
        ordering = ("event", "user")
    
    event = models.ForeignKey(
        EVENT,
        verbose_name=event_single,
        on_delete=models.CASCADE
    )  # type: Event
    
    ignore = models.BooleanField(
        default=False,
        verbose_name=_("Ignorieren"),
    )  # type: bool
    
    def __str__(self):
        return self.event
