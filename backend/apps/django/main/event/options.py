from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = [
    "ModificationTypeOptions"
]


class ModificationTypeOptions(models.TextChoices):
    REPLACEMENT = "REPLACEMENT", _("Vertretung")
    FREE_PERIOD = "FREE_PERIOD", _("Freistunde")
    SELF_LEARN = "SELF_LEARN", _("Selbstorganisiertes Lernen")
    ROOM_CHANGE = "ROOM_CHANGE", _("Raumänderung")
