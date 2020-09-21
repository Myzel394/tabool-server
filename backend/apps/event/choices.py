from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = [
    "EventTypeChoices"
]


class EventTypeChoices(models.IntegerChoices):
    SUBSTITUTE = 1, _("Vertretung")
    EVENT = 2, _("Event")
    FREE = 3, _("Frei")
    

