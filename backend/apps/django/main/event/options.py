from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = [
    "ModificationTypeOptions"
]


class ModificationTypeOptions(models.IntegerChoices):
    REPLACEMENT = 0, _("Vertretung")
    FREE_PERIOD = 1, _("Freistunde")
    SELF_LEARN = 2, _("Selbstorganisiertes Lernen")
    ROOM_CHANGE = 4, _("Raumänderung")
