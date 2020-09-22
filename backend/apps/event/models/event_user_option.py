from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models import RandomIDMixin

from .. import model_references, model_verbose_functions
from ..sub.subquerysets import EventUserOptionQuerySet
from ...utils.models import AssociatedUserMixin

__all__ = [
    "EventUserOption"
]


class EventUserOption(RandomIDMixin, AssociatedUserMixin):
    class Meta:
        verbose_name = _("Event-Benutzer-Einstellung")
        verbose_name_plural = _("Event-Benutzer-Einstellungen")
        unique_together = (
            ("event", "associated_user")
        )
    
    objects = EventUserOptionQuerySet.as_manager()
    
    event = models.OneToOneField(
        model_references.EVENT,
        verbose_name=model_verbose_functions.event_single,
        on_delete=models.CASCADE,
    )
    
    ignore = models.BooleanField(
        verbose_name=_("Ignorieren"),
        default=False,
    )
