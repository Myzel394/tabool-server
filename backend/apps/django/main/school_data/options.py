from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = [
    "GenderChoices"
]


class GenderChoices(models.IntegerChoices):
    MALE = 0, _("Männlich")
    FEMALE = 1, _("Weiblich")
    DIVERSE = 2, _("Divers")
    UNKNOWN = 3, _("Unbekannt")
