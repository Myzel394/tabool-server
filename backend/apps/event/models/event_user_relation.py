from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models import RandomIDMixin

from .. import model_references, model_verbose_functions
from ...utils.models import AssociatedUserMixin


class EventUserRelation(RandomIDMixin, AssociatedUserMixin):
    class Meta:
        verbose_name = _("Event-Benutzer-Bindung")
        verbose_name_plural = _("Event-Benutzer-Bindungen")
        unique_together = (
            ("event", "associated_user")
        )
    
    event = models.OneToOneField(
        model_references.EVENT,
        verbose_name=model_verbose_functions.event_single,
        on_delete=models.CASCADE,
    )
