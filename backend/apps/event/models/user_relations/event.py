from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models import RandomIDMixin

from apps.utils import UserModelRelationMixin
from ...public import model_references, model_verbose_functions

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
        model_references.EVENT,
        verbose_name=model_verbose_functions.event_single,
        on_delete=models.CASCADE,
    )
    
    ignore = models.BooleanField(
        default=False,
        verbose_name=_("Ignorieren")
    )
    
    attendance = models.BooleanField(
        default=True,
        verbose_name=_("Anwesend")
    )
